export type Document = {
    prefix: string
}

export type DocumentWithChildren = Document & {
    children?: DocumentWithChildren[]
}

export type Requirement = {
    id: string,
    text: string,
    reviewed: boolean
}