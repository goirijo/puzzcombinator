from __future__ import annotations
from typing import Protocol, runtime_checkable, TextIO, Iterable, TypeAlias, Union
from dataclasses import dataclass


@runtime_checkable
class FileRepresentable(Protocol):

    def to_file(self, fileobj: TextIO) -> None:
        ...


@dataclass
class _Metadata:
    label: str | None = None
    memo: str | None = None


class HexIdGenerator:
    """Just makes random looking labels for the Node class"""

    def __init__(self, width: int = 4, seed: int = 0):
        self._width = width
        self._mod = 16**width
        self._counter = 0
        self._mult = 1103515245
        self._add = seed

    def next(self) -> str:
        n = (self._counter * self._mult + self._add) % self._mod
        self._counter += 1
        return f"{n:0{self._width}x}"


class _HasMetadata:
    _metadata: _Metadata

    _idGenerator = HexIdGenerator(2)

    def __init__(self, *, label=None, memo=None):
        if label is None:
            label = self._next_label()

        self._metadata = _Metadata(label=label, memo=memo)

    @property
    def label(self):
        return self._metadata.label

    @property
    def memo(self):
        return self._metadata.memo

    @classmethod
    def _next_label(cls) -> str:
        return cls._idGenerator.next()

    def _repr_metadata(self) -> str:
        parts = []
        if self.label is not None:
            parts.append(f"label={self.label!r}")
        if self.memo is not None:
            parts.append(f"memo={self.memo!r}")
        return ", ".join(parts)


class Edge(_HasMetadata):
    """The Edge is an edge in the graph that represents the entire collection of puzzles. Each edge
    is associated with a piece of data that is (except for the start and end nodes)
    the output of a node, and the input of the next node.
    Data is combined at a node to complete the set of clues necessary to solve a single
    puzzle, which yields an output. This output is then input for another node."""

    def __init__(self,
                 content,
                 *,
                 label: str | None = None,
                 memo: str | None = None):
        """The content is the piece of data relevant for this particular edge. It can be basically
        anything, but it needs to have certain functions defined to generate visual representations
        of it

        Parameters
        ----------
        content : Anything you want, but it needs to have a to_file defined
        parent : The node this edge originates from
        child : The node this edge points to


        """
        super().__init__(label=label, memo=memo)

        if not isinstance(content, FileRepresentable):
            raise TypeError("content must implement to_file(fileobj)")
        self._content = content
        self._parent = None
        self._child = None

    def assign_parent(self, parent: Node) -> None:
        """Assign the given Node as the parent"""
        self._parent = parent

    def assign_child(self, child: Node) -> None:
        """Assign the given Node as the parent"""
        self._child = child

    def __repr__(self) -> str:
        parts = []
        meta = self._repr_metadata()

        if meta:
            parts.append(meta)

        return f"Edge({', '.join(parts)})"


EdgelikeInput: TypeAlias = Union[Edge, FileRepresentable]
EdgelikeIterable: TypeAlias = Iterable[EdgelikeInput]


class Node(_HasMetadata):
    """The Node represents one "step" in the collection of puzzles. This could be solving one
    particular puzzle, combining many pieces together to form a new object or hint, or moving to
    a particular location. Once all the nodes are connected in a complete map, the entire flow
    of the hunt is defined. Each Node tracks which Edges (which old data) are coming in and out.
    The Edges coming in are the hints or any other required data or objects needed to move to the
    next Node, while the output is the next bit of information needed to move the game forward"""

    def __init__(self,
                 ins: EdgelikeInput,
                 outs: EdgelikeInput,
                 *,
                 label: str | None = None,
                 memo: str | None = None):
        """The ins and outs are arrays of Edges

        Parameter
        ---------
        ins : [Iterable[Edge], the pieces necessary to move to the next step
        outs : [Iterable[Edge], one or more pieces that are needed to complete future Nodes
        label : str, optional (keyword-only), short tag for the node, randomly generated if None
        memo : str, optional (keyword-only), description of what should occur at the Node


        """
        super().__init__(label=label, memo=memo)

        self._incoming = type(self)._edges_from_iterable(ins)
        self._outgoing = type(self)._edges_from_iterable(outs)

        self._assign_self_as_edge_relations()

    @classmethod
    def reset_counter_width(width):
        """How many digits do you want on the label?"""
        _idGenerator = HexIdGenerator(width)

    @staticmethod
    def _wrap_into_edge(obj):
        """Just for easier construction. Converts whatever into an Edge"""
        if isinstance(obj, Edge):
            return obj
        return Edge(obj)

    @classmethod
    def _edges_from_iterable(cls, value):
        """Just makes sure vale is all Edges and turns it into a list

        Parameters
        ----------
        value : iterable full of Edge

        Returns
        -------
        List of Edges

        """
        return [cls._wrap_into_edge(e) for e in value]

    def _assign_self_as_edge_relations(self) -> None:
        """For each Edge, set self as the parent or child accordingly"""
        for e in self._outgoing:
            e.assign_parent(self)

        for e in self._incoming:
            e.assign_child(self)

    def __repr__(self) -> str:
        parts = []
        meta = self._repr_metadata()

        if meta:
            parts.append(meta)

        parts.append(f"in={len(self._incoming)}")
        parts.append(f"out={len(self._outgoing)}")

        args = ", ".join(parts)
        return f"{self.__class__.__name__}({args})"
