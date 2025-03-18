//
//  GetAllDepartmentsResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 18/03/2025.
//

import Vapor

struct GetAllDepartmentsResponse: BaseServerModel {
    var message: String
    var status: HTTPStatus
    var departments: [DepartmentModel]?
}
