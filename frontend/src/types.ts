export type ReqDocument = {
    prefix: string;
};

export type ReqDocumentWithChildren = ReqDocument & {
    children?: ReqDocumentWithChildren[];
};

export type Requirement = {
    id: string;
    text: string;
    reviewed: boolean;
    links: string[];
}

export type JWTToken = {
    token: string,
    exp: number,
    iat: number
} | null

export type RequirementWithDoc = Requirement & {
    docPrefix: string;
};
