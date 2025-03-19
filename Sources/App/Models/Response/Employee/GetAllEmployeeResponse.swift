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
    var employees: [EmployeeListRowResponse]?
}

//MARK: - GetSpecificEmploeeResponse -
struct GetSpecificEmploeeResponse: Content {
    var message: String
    var status: HTTPStatus
    var employee: EmployeeResponse?
}

//MARK: - EmployeeListRowResponse -
struct EmployeeListRowResponse: Content {
    var id: ObjectId?
    var name: String?
    var designation: DesignationModel?
    var email: String?
    var avatar: String?
}

//MARK: - EmployeeResponse -
struct EmployeeResponse: Content {
    var name: String?
    var email: String?
    var id: ObjectId?
    var designation: DesignationModel?
    var department: DepartmentModel?
    var avatar: String?
    var created_at: Date?
    var updated_at: Date?
    var emp_id: Int?
    var dob: Date?
    var date_of_joining: Date?
    var phone: String?
    var profiles: [GetProfileResponse]?
}
