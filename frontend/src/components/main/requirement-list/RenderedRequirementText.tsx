import { Typography } from "@mui/material";

export default function RenderedRequirementText({ text }: { text: string }) {
    return (
        <Typography variant="body1" sx={{ mt: 2 }}>
            {text}
        </Typography>
    );
}
