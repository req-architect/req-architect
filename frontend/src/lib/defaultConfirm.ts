import { confirmAlert } from "react-confirm-alert";

export function defaultConfirm(
    title: string,
    message: string,
    callback: () => void,
) {
    confirmAlert({
        title,
        message,
        buttons: [
            {
                label: "Yes",
                onClick: callback,
            },
            {
                label: "No",
                onClick: () => {},
            },
        ],
    });
}
