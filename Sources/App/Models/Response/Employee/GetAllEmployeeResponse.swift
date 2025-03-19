//
//  GetAllEmployeeResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor
@preconcurrency import FluentMongoDriver

//MARK: - GetAllEmployeeResponse -
struct GetAllEmployeeResponse: BaseServerModel {
    var message: String
    var status: HTTPStatus
    var employees: [EmployeeResponse]?
}

//MARK: - GetSpecificEmploeeResponse -
struct GetSpecificEmploeeResponse: Content {
    var message: String
    var status: HTTPStatus
    var employee: EmployeeResponse?
}

//MARK: - EmployeeResponse -
struct EmployeeResponse: Content {
    var name: String?
    var email: String?
    var id: ObjectId?
    var designation: DesignationModel?
    var department: DepartmentModel?
    var avatarURL: String?
    var created_at: Date?
    var updated_at: Date?
    var emp_id: Int?
}
