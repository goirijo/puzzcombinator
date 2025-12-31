from __future__ import annotations
from typing import Protocol, runtime_checkable, TextIO, Iterable, TypeAlias, Union

@runtime_checkable
class FileRepresentable(Protocol):
    def to_file(self, fileobj: TextIO) -> None:
        ...

class Edge(object):

    """The Edge is an edge in the graph that represents the entire collection of puzzles. Each edge
    is associated with a piece of data that is (except for the start and end nodes)
    the output of a node, and the input of the next node.
    Data is combined at a node to complete the set of clues necessary to solve a single
    puzzle, which yields an output. This output is then input for another node."""

    def __init__(self, content):
        """The content is the piece of data relevant for this particular edge. It can be basically
        anything, but it needs to have certain functions defined to generate visual representations
        of it

        Parameters
        ----------
        content : Anything you want, but it needs to have a to_file defined
        parent : The node this edge originates from
        child : The node this edge points to


        """
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


class HexIdGenerator:

    """Just makes random looking labels for the Node class"""

    def __init__(self, width: int = 4, seed: int = 0):
        self._width = width
        self._mod = 16 ** width
        self._counter = 0
        self._mult = 1103515245
        self._add = seed

    def next(self) -> str:
        n = (self._counter * self._mult + self._add) % self._mod
        self._counter += 1
        return f"{n:0{self._width}x}"



EdgelikeInput: TypeAlias = Union[Edge, FileRepresentable]
EdgelikeIterable: TypeAlias = Iterable[EdgelikeInput]

class Node(object):

    """The Node represents one "step" in the collection of puzzles. This could be solving one
    particular puzzle, combining many pieces together to form a new object or hint, or moving to
    a particular location. Once all the nodes are connected in a complete map, the entire flow
    of the hunt is defined. Each Node tracks which Edges (which old data) are coming in and out.
    The Edges coming in are the hints or any other required data or objects needed to move to the
    next Node, while the output is the next bit of information needed to move the game forward"""

    _idGenerator = HexIdGenerator(2)

    @classmethod
    def reset_counter_width(width):
        """How many digits do you want on the label?"""
        _idGenerator = HexIdGenerator(width)

    @classmethod
    def _next_label(cls) -> str:
        return cls._idGenerator.next()

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

    def __init__(self, ins: EdgelikeInput, outs: EdgelikeInput):
        """The ins and outs are arrays of Edges

        Parameter
        ---------
        ins : Array of Edges, the pieces necessary to move to the next step
        outs : Array of Edges, one or more pieces that are needed to complete future Nodes


        """
        self._incoming = type(self)._edges_from_iterable(ins)
        self._outgoing = type(self)._edges_from_iterable(outs)

        self._assign_self_as_edge_relations()

        self.label = self._next_label()
