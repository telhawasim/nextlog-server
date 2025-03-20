import Vapor

// configures your application
public func configure(_ app: Application) async throws {
    
    app.http.server.configuration.hostname = "192.168.31.221"
    app.http.server.configuration.port = 8080
    /// Configure JWT
    try await configureJWT(app)
    /// Middleware
    app.middleware.use(FileMiddleware(publicDirectory: app.directory.publicDirectory))
    /// Configure Database
    try configureDatabase(app)
    /// Configure Routes
    try routes(app)
}
