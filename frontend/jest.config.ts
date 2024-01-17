import { defaults } from "jest-config";

export default {
    bail: true,
    moduleFileExtensions: [...defaults.moduleFileExtensions, "ts", "tsx"],
    roots: ["src"],
    testMatch: ["<rootDir>/src/**/?(*.)test.{ts,tsx}"],
    transform: {
        "^.+\\.tsx?$": "ts-jest",
    },
    verbose: true,
};
