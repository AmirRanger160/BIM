// Vite plugin to handle SPA routing - fallback to index.html for all unknown routes
import fs from 'fs'
import path from 'path'

export default function spaFallback() {
  let config

  return {
    name: 'spa-fallback',
    apply: 'serve',
    enforce: 'post',
    configResolved(resolvedConfig) {
      config = resolvedConfig
    },
    configureServer(server) {
      return () => {
        server.middlewares.use((req, res, next) => {
          // Check if the request is for a file
          const filePath = path.join(config.root, 'index.html')
          
          // Skip if it's a static file request
          if (req.url.includes('.')) {
            return next()
          }
          
          // Skip API requests
          if (req.url.startsWith('/api')) {
            return next()
          }
          
          // Skip if file exists (Vite handles it)
          try {
            const fullPath = path.join(config.root, 'src', req.url)
            if (fs.existsSync(fullPath)) {
              return next()
            }
          } catch (e) {
            // Continue to fallback
          }
          
          // Serve index.html for all other routes
          res.setHeader('Content-Type', 'text/html; charset=utf-8')
          res.end(fs.readFileSync(filePath, 'utf-8'))
        })
      }
    }
  }
}
