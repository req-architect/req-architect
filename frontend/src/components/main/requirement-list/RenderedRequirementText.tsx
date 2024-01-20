import { Typography } from "@mui/material";

import plantumlEncoder from "plantuml-encoder";
import parseRequirementText, {
    RenderedRequirementComponent,
    RequirementParseError,
} from "../../../lib/parseRequirementText.ts";

/*
    This component is used to display the text of a requirement.
    It will parse the text and display it.
*/

function umlDiagramSrc(text: string) {
    return `https://www.plantuml.com/plantuml/svg/${plantumlEncoder.encode(
        text,
    )}`;
}

export default function RenderedRequirementText({ text }: { text: string }) {
    let parsedText: RenderedRequirementComponent[] = [];
    try {
        parsedText = parseRequirementText(text);
    } catch (e) {
        if (e instanceof RequirementParseError) {
            return (
                <Typography variant="body1" gutterBottom color="error">
                    {e.message}
                </Typography>
            );
        }
    }
    return parsedText.map((item, index) =>
        item.type === "text" ? (
            <Typography variant="body1" gutterBottom key={index}>
                {item.text}
            </Typography>
        ) : (
            <img
                src={umlDiagramSrc(item.text)}
                alt="UML diagram"
                width="100%"
                key={index}
            />
        ),
    );
}
