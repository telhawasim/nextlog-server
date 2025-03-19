//
//  GetAllAdminResponse.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor

struct GetAllAdminResponse: BaseServerModel {
    var message: String
    var status: HTTPStatus
    var admins: [AdminResponseModel]?
}
