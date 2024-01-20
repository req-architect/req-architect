import { RefObject, useEffect } from "react";

/*
    This hook is used to detect clicks inside a specific element.
    It is used to close the dropdown menu when the user clicks outside of it.
*/

export default function useClickInside(
    ref: RefObject<HTMLInputElement>,
    callback: () => void,
) {
    useEffect(() => {
        function handleClickInside(event: MouseEvent) {
            if (ref.current && ref.current.contains(event.target as Node)) {
                callback();
            }
        }
        // Bind the event listener
        document.addEventListener("mousedown", handleClickInside);
        return () => {
            // Unbind the event listener on clean up
            document.removeEventListener("mousedown", handleClickInside);
        };
    }, [ref, callback]);
}
