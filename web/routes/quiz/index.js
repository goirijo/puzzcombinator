import formbody from '@fastify/formbody'

export default async function (fastify) {
    await fastify.register(formbody)

    fastify.get('/:profileId', async (request, reply) => {
        const { profileId } = request.params

        // For now, just prove routing works
        reply
            .type('text/html')
            .send(`
      <h1>Profile ${profileId}</h1>
      <p>This is where the quiz will live.</p>

      <form method="POST" action="/quiz/${profileId}/answer">
        <button>Continue</button>
      </form>
    `)
    })

    fastify.post('/:profileId/answer', { bodyLimit: 1_000_000 }, async (request, reply) => {
        const { profileId } = request.params
        const { answer } = request.body   // formbody parses this automatically

        console.log(`Profile ${profileId} submitted: ${answer}`)

        reply.type('text/html').send(`
    <h1>Profile ${profileId}</h1>
    <p>Answer recorded: ${answer}</p>
    <form method="POST" action="/${profileId}/answer">
      <input name="answer" placeholder="Your answer">
      <button type="submit">Submit another</button>
    </form>
  `)
    })

    fastify.get('/:profileId/result', async (request) => {
        const { profileId } = request.params
        return `<h1>Result for ${profileId}</h1>`
    })
}

