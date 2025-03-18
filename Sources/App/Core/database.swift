//
//  database.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
import FluentMongoDriver

public func configureDatabase(_ app: Application) throws {
    try app.databases.use(.mongo(connectionString: "mongodb://localhost:27017/nextlog"), as: .mongo)
}
