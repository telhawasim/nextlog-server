//
//  JWTTokenPayload.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
import JWT
@preconcurrency import FluentMongoDriver

struct JWTTokenPayload: JWTPayload, Authenticatable {
    var id: ObjectId
    var isAdmin: Bool
    var exp: ExpirationClaim
    
    //MARK: - VERIFY -
    func verify(using algorithm: some JWTAlgorithm) async throws {
        try self.exp.verifyNotExpired()
    }
}
