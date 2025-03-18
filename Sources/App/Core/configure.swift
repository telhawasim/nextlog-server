import Vapor

// configures your application
public func configure(_ app: Application) async throws {
    /// Configure Database
    try configureDatabase(app)
    /// Configure Routes
    try routes(app)
}
