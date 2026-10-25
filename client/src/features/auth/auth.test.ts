import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { validateLoginInput } from "./auth-service";
import { mapTokenResponseDto, mapUserDto } from "./api";
import {
  getRoleDefaultPath,
  isPathAllowedForRole,
  isSafeRedirect,
} from "./use-login-form";
import { BackendTokenResponseDto, BackendUserDto } from "./types";

describe("validateLoginInput", () => {
  it("should succeed with valid email and password", () => {
    assert.doesNotThrow(() => {
      validateLoginInput({ email: "admin@pens.ac.id", password: "password123" });
    });
  });

  it("should throw error if email is empty", () => {
    assert.throws(
      () => {
        validateLoginInput({ email: "", password: "password123" });
      },
      { message: "Email wajib diisi" }
    );
  });

  it("should throw error if email format is invalid", () => {
    assert.throws(
      () => {
        validateLoginInput({ email: "not-an-email", password: "password123" });
      },
      { message: "Format email tidak valid" }
    );
  });

  it("should throw error if password is empty", () => {
    assert.throws(
      () => {
        validateLoginInput({ email: "admin@pens.ac.id", password: "" });
      },
      { message: "Password wajib diisi" }
    );
  });
});

describe("DTO mapping", () => {
  it("should map user DTO to domain user correctly", () => {
    const dto: BackendUserDto = {
      id: "u-1",
      email: "dosen@pens.ac.id",
      name: "Dr. Dosen",
      role: "lecturer",
      nip: "19800101",
      nrp: null,
      must_change_password: true,
    };
    const user = mapUserDto(dto);
    assert.equal(user.id, "u-1");
    assert.equal(user.email, "dosen@pens.ac.id");
    assert.equal(user.name, "Dr. Dosen");
    assert.equal(user.role, "lecturer");
    assert.equal(user.nip, "19800101");
    assert.equal(user.nrp, null);
    assert.equal(user.mustChangePassword, true);
  });

  it("should map token response DTO to domain session correctly", () => {
    const dto: BackendTokenResponseDto = {
      access_token: "access-token-123",
      refresh_token: "refresh-token-456",
      token_type: "bearer",
      must_change_password: false,
      user: {
        id: "u-2",
        email: "mhs@pens.ac.id",
        name: "Mahasiswa",
        role: "student",
        nip: null,
        nrp: "3123600001",
        must_change_password: false,
      },
    };
    const session = mapTokenResponseDto(dto);
    assert.equal(session.tokens.accessToken, "access-token-123");
    assert.equal(session.tokens.refreshToken, "refresh-token-456");
    assert.equal(session.tokens.tokenType, "bearer");
    assert.equal(session.user.role, "student");
    assert.equal(session.user.nrp, "3123600001");
  });
});

describe("Routing and Role Helpers", () => {
  it("should return correct role default paths", () => {
    assert.equal(getRoleDefaultPath("admin"), "/admin");
    assert.equal(getRoleDefaultPath("lecturer"), "/lecturer");
    assert.equal(getRoleDefaultPath("student"), "/student");
  });

  it("should identify safe and unsafe redirect paths", () => {
    assert.equal(isSafeRedirect("/admin"), true);
    assert.equal(isSafeRedirect("/student/history"), true);
    assert.equal(isSafeRedirect(null), false);
    assert.equal(isSafeRedirect(""), false);
    assert.equal(isSafeRedirect("https://attacker.com"), false);
    assert.equal(isSafeRedirect("//attacker.com"), false);
    assert.equal(isSafeRedirect("/\\attacker.com"), false);
    assert.equal(isSafeRedirect("javascript:alert(1)"), false);
  });

  it("should check role path authorization", () => {
    assert.equal(isPathAllowedForRole("/admin", "admin"), true);
    assert.equal(isPathAllowedForRole("/admin/users", "admin"), true);
    assert.equal(isPathAllowedForRole("/admin", "student"), false);
    assert.equal(isPathAllowedForRole("/lecturer", "lecturer"), true);
    assert.equal(isPathAllowedForRole("/lecturer", "student"), false);
    assert.equal(isPathAllowedForRole("/student", "student"), true);
    assert.equal(isPathAllowedForRole("/student", "lecturer"), false);
  });
});
