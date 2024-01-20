/* 
    Typescript types used in the frontend
*/

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
};

export type JWTToken = {
    token: string;
    exp: number;
    iat: number;
} | null;

export type RequirementWithDoc = Requirement & {
    docPrefix: string;
};

export type OAuthProvider = "gitlab" | "github";

export type AppUser = {
    provider: OAuthProvider;
    uid: string;
    login: string;
    email: string | null;
};
