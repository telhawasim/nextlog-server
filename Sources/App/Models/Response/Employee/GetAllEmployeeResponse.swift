//
//  GetAllEmployeeResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

struct GetAllEmployeeResponse: BaseServerModel {
    var message: String
    var status: HTTPStatus
    var employees: [EmployeeResponse]?
}

struct EmployeeResponse: Content {
    var name: String?
    var email: String?
    var id: ObjectId?
    var designation: DesignationModel?
    var department: DepartmentModel?
    var avatarURL: String?
}
