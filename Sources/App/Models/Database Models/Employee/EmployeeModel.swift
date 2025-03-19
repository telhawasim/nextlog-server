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
    @Field(key: "emp_id")
    var emp_id: Int
    @Field(key: "avatar")
    var avatar: String
    /// Designation
    @Parent(key: "designation")
    var designation: DesignationModel
    /// Department
    @Parent(key: "department")
    var department: DepartmentModel
    /// Date of Birth
    @Field(key: "dob")
    var dob: Date
    /// Phone
    @Field(key: "phone")
    var phone: String
    @Field(key: "date_of_joining")
    var date_of_joining: Date
    /// Created At
    @Field(key: "created_at")
    var created_at: Date
    /// Updated At
    @Field(key: "updated_at")
    var updated_at: Date
    
    init() { }
    
    /// Initializer 
    init(
        id: ObjectId? = nil,
        name: String,
        email: String,
        emp_id: Int,
        avatar: String,
        designation: ObjectId,
        department: ObjectId,
        dob: Date,
        phone: String,
        date_of_joining: Date,
        created_at: Date = Date(),
        updated_at: Date = Date()
    ) {
        self.id = id
        self.name = name
        self.email = email
        self.emp_id = emp_id
        self.avatar = avatar
        self.$designation.id = designation
        self.$department.id = department
        self.dob = dob
        self.phone = phone
        self.date_of_joining = date_of_joining
        self.created_at = created_at
        self.updated_at = updated_at
    }
}
