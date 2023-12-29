import { render } from "@testing-library/react";
import MainPageHeader from "../../../components/main/MainPageHeader.tsx";

test("render main page header", () => {
    const { getByText } = render(<MainPageHeader />);
    const typographyElement = getByText(/PZSP2-KUKIWAKO/i);
    expect(typographyElement).not.toBeFalsy();
});
