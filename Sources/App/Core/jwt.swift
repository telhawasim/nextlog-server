//
//  jwt.swift
//  Nextlog-server
//
//  Created by Telha Wasim on 19/03/2025.
//

import Vapor
import JWT

public func configureJWT(_ app: Application) async throws {
    await app.jwt.keys.add(hmac: "secret", digestAlgorithm: .sha256)
}
