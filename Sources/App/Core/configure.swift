import Vapor

// configures your application
public func configure(_ app: Application) async throws {
    app.middleware.use(FileMiddleware(publicDirectory: app.directory.publicDirectory))
    /// Configure Database
    try configureDatabase(app)
    /// Configure Routes
    try routes(app)
}
