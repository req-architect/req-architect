import { expect, test, describe } from "@jest/globals";
import parseRequirementText, {
    RequirementParseError,
} from "../../lib/parseRequirementText.ts";

describe("test parseRequirementText", () => {
    test("empty string", () => {
        expect(parseRequirementText("")).toStrictEqual([]);
    });
    test("text only", () => {
        expect(parseRequirementText("hello world")).toStrictEqual([
            { type: "text", text: "hello world" },
        ]);
    });
    test("paragraph", () => {
        expect(parseRequirementText("hello\nworld")).toStrictEqual([
            { type: "text", text: "hello\nworld" },
        ]);
    });
    test("uml only", () => {
        expect(
            parseRequirementText('@startuml\ncomponent "Browser"\n@enduml'),
        ).toStrictEqual([
            { type: "uml", text: '@startuml\ncomponent "Browser"\n@enduml' },
        ]);
    });
    test("uml and text", () => {
        expect(
            parseRequirementText(
                'hello world\n@startuml\ncomponent "Browser"\n@enduml',
            ),
        ).toStrictEqual([
            { type: "text", text: "hello world" },
            { type: "uml", text: '@startuml\ncomponent "Browser"\n@enduml' },
        ]);
    });
    test("embedded uml", () => {
        expect(
            parseRequirementText(
                'hello world\n@startuml\ncomponent "Browser"\n@enduml\nhello world',
            ),
        ).toStrictEqual([
            { type: "text", text: "hello world" },
            { type: "uml", text: '@startuml\ncomponent "Browser"\n@enduml' },
            { type: "text", text: "hello world" },
        ]);
    });
    test("no UML ending", () => {
        expect(() =>
            parseRequirementText("@startuml\ncomponent Browser"),
        ).toThrow(RequirementParseError);
    });
    test("embedded uml in uml", () => {
        expect(() =>
            parseRequirementText(
                '@startuml\ncomponent "Browser"\n@startuml\ncomponent "Hello"\n@enduml\n@enduml',
            ),
        ).toThrow(RequirementParseError);
    });
    test("uml end without start", () => {
        expect(() => parseRequirementText("hello\n@enduml")).toThrow(
            RequirementParseError,
        );
    });
});
