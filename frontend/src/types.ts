export type ReqDocument = {
    prefix: string
}

export type ReqDocumentWithChildren = ReqDocument & {
    children?: ReqDocumentWithChildren[]
}

export type Requirement = {
    id: string,
    text: string,
    reviewed: boolean
}

export type JWTToken = {
    token: string,
    exp: number,
    iat: number
} | null