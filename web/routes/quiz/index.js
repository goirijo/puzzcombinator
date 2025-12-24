'use strict'

module.exports = async function (fastify) {

  // GET /quiz/:profileId
  fastify.get('/:profileId', async function (request, reply) {
    return reply.view('quiz/quiz.ejs', {
      profileId: request.params.profileId,
      answer: null,
      basePath: 'quiz'  // pass the prefix
    })
  })

  // POST /quiz/:profileId/answer
  fastify.post('/:profileId/answer', async function (request, reply) {
    const { profileId } = request.params
    const { answer } = request.body

    return reply.view('quiz/quiz.ejs', {
      profileId,
      answer,
      basePath: 'quiz'  // same prefix
    })
  })

}

