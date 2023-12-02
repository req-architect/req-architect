import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

export default function RepoList() {
  const options = repositories.map((option) => {
    const firstLetter = option.label[0].toUpperCase();
    return {
      firstLetter: /[0-9]/.test(firstLetter) ? "0-9" : firstLetter,
      ...option,
    };
  });

  return (
    <Autocomplete
      disablePortal
      renderInput={(params) => <TextField {...params} label="Repository" />}
      options={options.sort(
        (a, b) => -b.firstLetter.localeCompare(a.firstLetter)
      )}
      groupBy={(option) => option.firstLetter}
      sx={{ width: "70%" }}
    />
  );
}

const repositories = [{ label: "PZSP2-KUKIWAKO" }, { label: "IUM" }];
