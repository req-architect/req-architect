import { confirmAlert } from "react-confirm-alert";

/*
    This function is used to display a default confirmation dialog.
    It is used to confirm the deletion of a requirement.
*/

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
