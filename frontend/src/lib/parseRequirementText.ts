export type RenderedRequirementComponent = {
    type: "text" | "uml";
    text: string;
};

export class RequirementParseError extends Error {
    constructor(message: string) {
        super(message);
    }
}

export default function parseRequirementText(text: string) {
    let buffer: string = "";
    function pushToBuffer(line: string) {
        if (buffer.length == 0) {
            buffer = line;
        } else {
            buffer += "\n" + line;
        }
    }
    let inUml: boolean = false;
    const result: RenderedRequirementComponent[] = [];
    for (const line of text.split(/\r?\n/)) {
        if (line.startsWith("@startuml")) {
            if (inUml) {
                throw new RequirementParseError(
                    "Embedding UML diagrams is not supported",
                );
            }
            if (buffer.length > 0) {
                result.push({ type: "text", text: buffer });
            }
            buffer = line;
            inUml = true;
        } else if (line.startsWith("@enduml")) {
            if (!inUml) {
                throw new RequirementParseError(
                    "UML diagram end without start",
                );
            }
            pushToBuffer(line);
            result.push({ type: "uml", text: buffer });
            buffer = "";
            inUml = false;
        } else if (line.length > 0) {
            pushToBuffer(line);
        }
    }
    if (inUml) {
        throw new RequirementParseError("UML diagram start without end");
    }
    if (buffer.length > 0) {
        result.push({ type: "text", text: buffer });
    }
    return result;
}
