import MainPageHeader from "../components/MainPageHeader.tsx";
import DocumentList from "../components/DocumentList.tsx";
import RequirementList from "../components/RequirementList.tsx";
import RequirementDetails from "../components/RequirementDetails.tsx";

export default function MainPage() {
    return (
        <>
            <MainPageHeader/>
            <DocumentList/>
            <RequirementList/>
            <RequirementDetails/>
        </>
    )
}
