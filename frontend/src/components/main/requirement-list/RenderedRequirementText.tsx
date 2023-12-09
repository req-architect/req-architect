import { Typography } from "@mui/material";

export default function RenderedRequirementText({ text }: { text: string }) {
    return (
        <Typography variant="body1" whiteSpace={"pre-line"} sx={{ }}>
            {text}
        </Typography>
    );
}
