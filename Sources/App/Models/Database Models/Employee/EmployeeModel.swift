//
//  EmployeeModel.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Foundation
import Vapor
import Fluent
@preconcurrency import FluentMongoDriver

final class EmployeeModel: Model, Content, @unchecked Sendable {
    
    static let schema = "employees"
    
    /// ID
    @ID(custom: "_id")
    var id: ObjectId?
    /// Name
    @Field(key: "name")
    var name: String
    /// Email
    @Field(key: "email")
    var email: String
    /// Avatar
    @Field(key: "avatar")
    var avatar: String
    
    @Parent(key: "designation")
    var designation: DesignationModel
    
    @Parent(key: "department")
    var department: DepartmentModel
    
    init() { }
    
    /// Initializer 
    init(id: ObjectId? = nil, name: String, email: String, avatar: String, designation: ObjectId, department: ObjectId) {
        self.id = id
        self.name = name
        self.email = email
        self.avatar = avatar
        self.$designation.id = designation
        self.$department.id = department
    }
}
