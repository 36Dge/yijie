// Read-only native AX evidence, using the user's existing AX authorization.
// No page evaluation, input synthesis, permissions, or process signals.
import AppKit
import ApplicationServices
import Darwin

guard (2...3).contains(CommandLine.arguments.count), let pid = pid_t(CommandLine.arguments[1]) else { exit(2) }
let inspector = CommandLine.arguments.count == 3 && CommandLine.arguments[2] == "inspector"
let expected = "/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI.app/Contents/MacOS/yijie-desktop"
var path = [CChar](repeating: 0, count: 4 * Int(MAXPATHLEN))
guard proc_pidpath(pid, &path, UInt32(path.count)) > 0, String(cString: path) == expected,
      AXIsProcessTrusted() else { fputs("Expected authorized packaged process unavailable\n", stderr); exit(2) }
func attr(_ item: AXUIElement, _ key: String) -> CFTypeRef? {
    var value: CFTypeRef?
    return AXUIElementCopyAttributeValue(item, key as CFString, &value) == .success ? value : nil
}
func str(_ item: AXUIElement, _ key: String) -> String {
    guard let value = attr(item, key) else { return "" }
    return String(describing: value)
}
let app = AXUIElementCreateApplication(pid)
let windows = attr(app, kAXWindowsAttribute) as? [AXUIElement] ?? []
let matches = windows.filter { inspector ? str($0, kAXTitleAttribute).hasPrefix("Web Inspector — ") : str($0, kAXTitleAttribute) == "易界 AI" }
guard matches.count == 1 else { fputs("Expected one main App window\n", stderr); exit(2) }
var rows: [[String: Any]] = []
var truncated = false
func walk(_ item: AXUIElement, _ depth: Int) {
    guard depth < 40, rows.count < 5000 else { truncated = true; return }
    if str(item, kAXDescriptionAttribute) == "主导航" { return }
    var row: [String: Any] = ["depth": depth]
    for (key, field) in [("role", kAXRoleAttribute), ("title", kAXTitleAttribute),
                         ("description", kAXDescriptionAttribute), ("value", kAXValueAttribute),
                         ("focused", kAXFocusedAttribute), ("enabled", kAXEnabledAttribute)] {
        let value = str(item, field)
        if !value.isEmpty { row[key] = value }
    }
    rows.append(row)
    for child in attr(item, kAXChildrenAttribute) as? [AXUIElement] ?? [] { walk(child, depth + 1) }
}
walk(matches[0], 0)
let result: [String: Any] = ["pid": pid, "nodes": rows, "truncated": truncated,
    "scope": "Actual native AX roles, labels, values and focus; excludes main navigation. No heap or port observation.", "inspector": inspector]
let data = try JSONSerialization.data(withJSONObject: result, options: [.sortedKeys])
print(String(decoding: data, as: UTF8.self))
