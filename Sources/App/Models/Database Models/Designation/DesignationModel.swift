//
//  DesignationModel.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
@preconcurrency import FluentMongoDriver

final class DesignationModel: Model, @unchecked Sendable {
    
    /// Schema
    static let schema: String = "designations"
    /// ID
    @ID(custom: "_id")
    var id: ObjectId?
    /// Name
    @Field(key: "name")
    var name: String
    
    init() { }
    
    /// Initializer
    init(id: ObjectId? = nil, name: String) {
        self.id = id
        self.name = name
    }
}
