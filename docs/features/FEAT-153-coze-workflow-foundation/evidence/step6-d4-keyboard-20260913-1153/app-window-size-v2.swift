// Proposed UI-only helper. Do not execute without explicit authorization to
// replace CUA with macOS AX/CGEvent for this exact dev process.
// Does not inject code, invoke Tauri/API business operations, alter permissions,
// replace executable files, or send process termination signals.
import AppKit
import ApplicationServices
import ScreenCaptureKit
import ImageIO
import UniformTypeIdentifiers
import Darwin

let nativeApplication = NSApplication.shared
nativeApplication.setActivationPolicy(.prohibited)

let targetPID: pid_t = 12569
let expectedExecutable = "/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI.app/Contents/MacOS/yijie-desktop"
let evidenceRoot = "/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/docs/features/FEAT-153-coze-workflow-foundation/evidence/step6-d4-keyboard-20260913-1153/"

struct Stop: Error { let message: String }
func require(_ value: Bool, _ message: String) throws {
    if !value { throw Stop(message: message) }
}
func identity() throws {
    // SDK sys/proc_info.h defines PROC_PIDPATHINFO_MAXSIZE as 4*MAXPATHLEN;
    // this expression macro is not imported into Swift.
    var path = [CChar](repeating: 0, count: 4 * Int(MAXPATHLEN))
    let length = proc_pidpath(targetPID, &path, UInt32(path.count))
    try require(length > 0 && String(cString: path) == expectedExecutable, "Target process identity differs; no action sent")
}
func attribute(_ element: AXUIElement, _ name: String) -> CFTypeRef? {
    var value: CFTypeRef?
    return AXUIElementCopyAttributeValue(element, name as CFString, &value) == .success ? value : nil
}
func string(_ element: AXUIElement, _ name: String) -> String {
    guard let value = attribute(element, name) else { return "" }
    return String(describing: value).prefix(700).description
}
func window() throws -> (AXUIElement, CGRect) {
    try identity()
    try require(AXIsProcessTrusted(), "Existing Accessibility access unavailable; no permission changed")
    let application = AXUIElementCreateApplication(targetPID)
    let windows = attribute(application, kAXWindowsAttribute) as? [AXUIElement] ?? []
    let matches = windows.filter { string($0, kAXTitleAttribute) == "易界 AI" }
    try require(matches.count == 1, "Expected one 易界 AI window; observe before acting")
    let selected = matches[0]
    guard let position = attribute(selected, kAXPositionAttribute),
          let size = attribute(selected, kAXSizeAttribute) else { throw Stop(message: "No window geometry") }
    try require(CFGetTypeID(position) == AXValueGetTypeID() && CFGetTypeID(size) == AXValueGetTypeID(), "Unexpected geometry type")
    var point = CGPoint.zero
    var dimensions = CGSize.zero
    try require(AXValueGetValue(position as! AXValue, .cgPoint, &point)
        && AXValueGetValue(size as! AXValue, .cgSize, &dimensions), "Window geometry could not be read")
    return (selected, CGRect(origin: point, size: dimensions))
}
func foreground() throws {
    try identity()
    try require(NSWorkspace.shared.frontmostApplication?.processIdentifier == targetPID, "Dev is not foreground; no input sent")
}
@MainActor func activate() async throws {
    try identity()
    guard let application = NSRunningApplication(processIdentifier: targetPID) else { throw Stop(message: "Dev process unavailable") }
    try require(application.activate(options: [.activateAllWindows]), "Normal application activation was declined")
    for _ in 0..<30 {
        if NSWorkspace.shared.frontmostApplication?.processIdentifier == targetPID { return }
        try await Task.sleep(nanoseconds: 50_000_000)
    }
    try foreground()
}
func json(_ value: Any) throws {
    let data = try JSONSerialization.data(withJSONObject: value, options: [.sortedKeys])
    print(String(decoding: data, as: UTF8.self))
}
func snapshot(_ root: AXUIElement, _ bounds: CGRect) throws {
    var nodes: [[String: Any]] = []
    func walk(_ element: AXUIElement, _ depth: Int) {
        guard depth < 20 && nodes.count < 1600 else { return }
        var node: [String: Any] = ["index": nodes.count, "depth": depth]
        for (key, field) in [("role", kAXRoleAttribute), ("title", kAXTitleAttribute),
                             ("description", kAXDescriptionAttribute), ("value", kAXValueAttribute), ("focused", kAXFocusedAttribute), ("enabled", kAXEnabledAttribute)] {
            let value = string(element, field)
            if !value.isEmpty { node[key] = value }
        }
        nodes.append(node)
        for child in attribute(element, kAXChildrenAttribute) as? [AXUIElement] ?? [] { walk(child, depth + 1) }
    }
    walk(root, 0)
    try json(["event_access": CGPreflightPostEventAccess(), "frontmost_pid": NSWorkspace.shared.frontmostApplication?.processIdentifier ?? -1, "pid": targetPID, "window": ["x": bounds.minX, "y": bounds.minY, "width": bounds.width, "height": bounds.height], "nodes": nodes])
}
func point(_ x: String, _ y: String, _ bounds: CGRect) throws -> CGPoint {
    guard let a = Double(x), let b = Double(y) else { throw Stop(message: "Expected window-relative coordinates") }
    try require(a >= 0 && b >= 0 && a < bounds.width && b < bounds.height, "Input coordinates outside target window")
    return CGPoint(x: bounds.minX + a, y: bounds.minY + b)
}
func mouse(_ kind: CGEventType, _ point: CGPoint) throws {
    try foreground()
    guard let event = CGEvent(mouseEventSource: nil, mouseType: kind, mouseCursorPosition: point, mouseButton: .left) else { throw Stop(message: "Mouse event unavailable") }
    event.post(tap: .cghidEventTap)
}
func key(_ name: String) throws {
    try foreground()
    let keys: [String: CGKeyCode] = ["tab": 48, "enter": 36, "escape": 53, "a": 0, "q": 12, "left": 123, "right": 124, "up": 126, "down": 125]
    let parts = name.split(separator: "+").map(String.init)
    guard let code = keys[parts.last ?? ""] else { throw Stop(message: "Unsupported key") }
    try require(parts.dropLast().allSatisfy { ["cmd", "shift"].contains($0) }, "Unsupported modifier")
    var flags: CGEventFlags = []
    if parts.contains("cmd") { flags.insert(.maskCommand) }
    if parts.contains("shift") { flags.insert(.maskShift) }
    for down in [true, false] {
        guard let event = CGEvent(keyboardEventSource: nil, virtualKey: code, keyDown: down) else { throw Stop(message: "Keyboard event unavailable") }
        event.flags = down ? flags : []
        event.post(tap: .cghidEventTap)
    }
}
func text(_ value: String) throws {
    try foreground()
    let units = Array(value.utf16)
    try require(units.count <= 4096, "Text exceeds helper limit")
    for down in [true, false] {
        guard let event = CGEvent(keyboardEventSource: nil, virtualKey: 0, keyDown: down) else { throw Stop(message: "Keyboard event unavailable") }
        event.flags = []
        event.keyboardSetUnicodeString(stringLength: units.count, unicodeString: units)
        event.post(tap: .cghidEventTap)
    }
}
@MainActor func resize() throws {
    let args=Array(CommandLine.arguments.dropFirst())
    try require(args.count==2, "Expected authorized window size")
    guard let width=Double(args[0]), let height=Double(args[1]) else { throw Stop(message: "Bad size") }
    try require((width==1180 && height==760) || (width==1440 && height==900), "Only the two authorized sizes")
    let (root, _)=try window()
    var origin=CGPoint(x:width==1440 ? 100 : 166,y:56)
    try require(AXUIElementSetAttributeValue(root,kAXPositionAttribute as CFString,AXValueCreate(.cgPoint,&origin)!) == .success, "Normal AX window positioning declined")
    var size=CGSize(width:width,height:height)
    try require(AXUIElementSetAttributeValue(root,kAXSizeAttribute as CFString,AXValueCreate(.cgSize,&size)!) == .success, "Normal AX window resize declined")
    let (_,bounds)=try window()
    try json(["pid":targetPID,"requested":[width,height],"actual":[bounds.width,bounds.height]])
}
Task { @MainActor in
    do { try resize(); exit(0) } catch { fputs("WINDOW_SIZE_STOP: normal resize did not complete\n",stderr); exit(1) }
}
dispatchMain()
