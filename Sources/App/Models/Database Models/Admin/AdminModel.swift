//
//  AdminModel.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
import Fluent
@preconcurrency import FluentMongoDriver

final class AdminModel: Model, @unchecked Sendable {
    
    /// Schema
    static let schema: String = "admins"
    /// ID
    @ID(custom: "_id")
    var id: ObjectId?
    /// Email
    @Field(key: "email")
    var email: String
    /// Password
    @Field(key: "password")
    var password: String
    /// Role
    @Field(key: "role")
    var role: String
    
    init() { }
    
    /// Initializer 
    init(id: ObjectId? = nil, email: String, password: String, role: String) {
        self.id = id
        self.email = email
        self.password = password
        self.role = role
    }
}
