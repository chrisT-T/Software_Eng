export const breakPointClassName = "monaco-editor-breakpoint";
export const shadowBreakpointClassName = "monaco-editor-breakpoint-shadow";
export const focusLineClassName = "monaco-editor-focus-line";
export const suffixTypeDict = new Map<string, string>([
  ["cpp", "cpp"],
  ["c", "c"],
  ["h", "c"],
  ["hpp", "cpp"],
  ["py", "python"],
  ["java", "java"],
  ["cs", "csharp"],
  ["css", "css"],
  ["html", "html"],
  ["js", "javascript"],
  ["ts", "typescript"],
  ["json", "json"],
  ["lua", "lua"],
  ["go", "go"],
  ["pl", "perl"],
  ["php", "php"],
  ["txt", "plaintext"],
  ["r", "r"],
  ["rs", "rust"],
  ["rb", "ruby"],
  ["sh", "shell"],
  ["swift", "swift"],
  ["xml", "xml"],
  ["yml", "yaml"],
  ["yaml", "yaml"],
  ["scss", "scss"],
  ["v", "verilog"],
  ["md", "markdown"],
]);
export const nameTypeDict = new Map([["dockerfile", "dockerfile"]]);

export const cssRule = [
  ".yRemoteSelection .yRemoteSelection-clientID { background-color: randomcolor;}",
  `.yRemoteSelectionHead .yRemoteSelectionHead-clientID {
  position: absolute;
  border-left: randomcolor solid 2px;
  border-top: randomcolor solid 2px;
  border-bottom: randomcolor solid 2px;
  height: 100%;
  box-sizing: border-box;
}`,
  `.yRemoteSelectionHead .yRemoteSelectionHead-clientID::after {
  position: absolute;
  content: " ";
  border: 3px solid randomcolor;
  border-radius: 4px;
  left: -4px;
  top: -5px;
}`,
];
