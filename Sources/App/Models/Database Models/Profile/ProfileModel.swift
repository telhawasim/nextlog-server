//
//  ProfileModel.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
import Fluent
@preconcurrency import FluentMongoDriver

final class ProfileModel: Model, @unchecked Sendable {
    
    /// Schema
    static let schema: String = "profiles"
    /// ID
    @ID(custom: "_id")
    var id: ObjectId?
    /// Name
    @Field(key: "name")
    var name: String
    /// Employee ID
    @Parent(key: "employee_id")
    var employee: EmployeeModel
    
    init() { }
    
    /// Initializer
    init(id: ObjectId? = nil, name: String, employeeID: ObjectId) {
        self.id = id
        self.name = name
        self.$employee.id = employeeID
    }
}
