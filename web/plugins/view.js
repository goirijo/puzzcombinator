'use strict'

const path = require('node:path')
const fp = require('fastify-plugin')
const view = require('@fastify/view')
const ejs = require('ejs')
const formbody = require('@fastify/formbody')

module.exports = fp(async function (fastify) {
  // Parse application/x-www-form-urlencoded
  fastify.register(formbody)

  // Enable server-side templates
  fastify.register(view, {
    engine: { ejs },
    root: path.join(__dirname, '..', 'views')
  })
})

