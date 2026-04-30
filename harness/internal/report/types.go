package report

type FindingType string

const (
	TypeMissingSnippet      FindingType = "MISSING_SNIPPET"
	TypeDocMissing          FindingType = "DOC_MISSING"
	TypeAscPageInvalid      FindingType = "ASC_PAGE_INVALID"
	TypeDocSurfaceDrift     FindingType = "DOC_SURFACE_DRIFT"
	TypeSnippetContentDrift FindingType = "SNIPPET_CONTENT_DRIFT"
	TypeDocPageStaleImport  FindingType = "DOC_PAGE_STALE_IMPORT"
)

type FindingStatus string

const (
	StatusOpen       FindingStatus = "open"
	StatusFixed      FindingStatus = "fixed"
	StatusNeedsHuman FindingStatus = "needs_human"
)

type Evidence struct {
	BeforeHash        string `json:"before_hash,omitempty"`
	AfterHash         string `json:"after_hash"`
	Artifact          string `json:"artifact"`
	CompileResult     string `json:"compile_result"`
	CompileOutputHash string `json:"compile_output_hash"`
}

type Finding struct {
	ID                   string        `json:"id"`
	Type                 FindingType   `json:"type"`
	Platform             string        `json:"platform"`
	FunctionID           string        `json:"function_id,omitempty"`
	SnippetFile          string        `json:"snippet_file,omitempty"`
	DocPage              string        `json:"doc_page,omitempty"`
	DocPageFile          string        `json:"doc_page_file,omitempty"`
	GendocsKey           string        `json:"gendocs_key,omitempty"`
	GendocsPath          string        `json:"gendocs_path,omitempty"`
	HasHardcodedCodeGroup bool         `json:"has_hardcoded_code_group,omitempty"`
	Detail               string        `json:"detail,omitempty"`
	Status               FindingStatus `json:"status"`
	Evidence             *Evidence     `json:"evidence,omitempty"`
}

type Summary struct {
	Open       int `json:"open"`
	Fixed      int `json:"fixed"`
	NeedsHuman int `json:"needs_human"`
}

type Report struct {
	GeneratedAt string    `json:"generated_at"`
	Summary     Summary   `json:"summary"`
	Findings    []Finding `json:"findings"`
}

func (r *Report) Recount() {
	r.Summary = Summary{}
	for _, f := range r.Findings {
		switch f.Status {
		case StatusOpen:
			r.Summary.Open++
		case StatusFixed:
			r.Summary.Fixed++
		case StatusNeedsHuman:
			r.Summary.NeedsHuman++
		}
	}
}
