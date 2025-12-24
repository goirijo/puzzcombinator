'use strict'

const fp = require('fastify-plugin')

module.exports = fp(async function (fastify) {
  // Add a decorator to compute base path for the current route
  fastify.decorateReply('renderView', function (template, data = {}) {
    // Compute base path from the route prefix, default to empty
    // request.routerPath is Fastify's internal route path
    const basePath = this.context.configPrefix || ''
    return this.view(template, { ...data, basePath })
  })
})

