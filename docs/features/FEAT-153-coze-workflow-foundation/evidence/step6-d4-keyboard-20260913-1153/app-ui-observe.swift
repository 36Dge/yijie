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
@MainActor func run() async throws {
    let args = Array(CommandLine.arguments.dropFirst())
    try require(!args.isEmpty, "Expected snapshot, screenshot, activate, click, drag, scroll, key or text")
    try require(["snapshot", "screenshot"].contains(args[0]), "Read-only packaged observer")
    let (root, bounds) = try window()
    if ["click", "drag", "key", "text", "scroll"].contains(args[0]) {
        try foreground()
    }
    switch args[0] {
    case "snapshot": try require(args.count == 1, "Wrong arguments"); try snapshot(root, bounds)
    case "activate": try require(args.count == 1, "Wrong arguments"); try await activate(); try json(["activated": targetPID])
    case "press", "press-outer", "focus", "fill":
        try require(args.count == (args[0] == "fill" ? 3 : 2), "Expected unique observed control title")
        var matches: [AXUIElement] = []
        var count = 0
        func find(_ item: AXUIElement, _ depth: Int) {
            guard depth < 20 && count < 1600 else { return }; count += 1
            let role = string(item, kAXRoleAttribute)
            if (["focus", "fill"].contains(args[0]) ? ["AXTextField", "AXTextArea"] : ["AXButton", "AXLink", "AXDisclosureTriangle", "AXCheckBox"]).contains(role) && string(item, kAXTitleAttribute) == args[1] { matches.append(item) }
            for child in attribute(item, kAXChildrenAttribute) as? [AXUIElement] ?? [] { find(child, depth + 1) }
        }
        find(root, 0)
        try require(args[0] == "press-outer" ? (args[1] == "返回工作流" && matches.count == 2) : matches.count == 1, "Expected observed matching control count")
        if args[0] == "fill" {
            try require(AXUIElementSetAttributeValue(matches[0], kAXFocusedAttribute as CFString, kCFBooleanTrue) == .success, "Native focus declined")
            try await Task.sleep(nanoseconds: 150_000_000)
            try require(args[2].utf16.count <= 4096, "Text limit")
            try require(AXUIElementSetAttributeValue(matches[0], kAXValueAttribute as CFString, args[2] as CFString) == .success, "Native accessibility value edit declined")
        } else if args[0] == "focus" {
            try require(AXUIElementSetAttributeValue(matches[0], kAXFocusedAttribute as CFString, kCFBooleanTrue) == .success, "Native accessibility focus declined")
        } else {
            try require(AXUIElementPerformAction(matches[0], kAXPressAction as CFString) == .success, "Native accessibility press declined")
        }
    case "click":
        try require(args.count == 3, "Wrong arguments")
        let p = try point(args[1], args[2], bounds)
        try mouse(.leftMouseDown, p); try mouse(.leftMouseUp, p)
    case "drag":
        try require(args.count == 5, "Wrong arguments")
        let a = try point(args[1], args[2], bounds), b = try point(args[3], args[4], bounds)
        try mouse(.leftMouseDown, a)
        // Release this helper's own mouse press even if foreground changes.
        var released = false
        defer { if !released { CGEvent(mouseEventSource: nil, mouseType: .leftMouseUp, mouseCursorPosition: b, mouseButton: .left)?.postToPid(targetPID) } }
        try await Task.sleep(nanoseconds: 100_000_000)
        for step in 1...18 {
            let t = Double(step) / 18
            try mouse(.leftMouseDragged, CGPoint(x: a.x + (b.x-a.x)*t, y: a.y + (b.y-a.y)*t))
            try await Task.sleep(nanoseconds: 20_000_000)
        }
        try mouse(.leftMouseUp, b); released = true
    case "key": try require(args.count == 2, "Wrong arguments"); try key(args[1])
    case "text": try require(args.count == 2, "Wrong arguments"); try text(args[1])
    case "scroll":
        try require(args.count == 4, "Wrong arguments")
        let p = try point(args[1], args[2], bounds)
        guard let amount = Int32(args[3]) else { throw Stop(message: "Expected bounded scroll amount") }
        try require(amount >= -1000 && amount <= 1000, "Scroll amount outside helper limit")
        try foreground()
        guard let event = CGEvent(scrollWheelEvent2Source: nil, units: .pixel, wheelCount: 1,
                                  wheel1: amount, wheel2: 0, wheel3: 0) else { throw Stop(message: "Scroll event unavailable") }
        event.location = p
        event.post(tap: .cghidEventTap)
    case "screenshot":
        try require(args.count == 2 && args[1].range(of: "^[a-z0-9-]+\\.png$", options: .regularExpression) != nil, "Expected an evidence PNG basename")
        let destination = URL(fileURLWithPath: evidenceRoot + args[1])
        try require(!FileManager.default.fileExists(atPath: destination.path), "Evidence target already exists")
        let content = try await SCShareableContent.excludingDesktopWindows(true, onScreenWindowsOnly: true)
        let choices = content.windows.filter { $0.owningApplication?.processID == targetPID && $0.title == "易界 AI" }
        try require(choices.count == 1, "Expected one on-screen dev window")
        let filter = SCContentFilter(desktopIndependentWindow: choices[0])
        let config = SCStreamConfiguration()
        config.width = Int(bounds.width); config.height = Int(bounds.height)
        config.showsCursor = false; config.ignoreShadowsSingleWindow = true
        let image = try await SCScreenshotManager.captureImage(contentFilter: filter, configuration: config)
        try identity()
        guard let output = CGImageDestinationCreateWithURL(destination as CFURL, UTType.png.identifier as CFString, 1, nil) else { throw Stop(message: "PNG destination unavailable") }
        CGImageDestinationAddImage(output, image, nil)
        try require(CGImageDestinationFinalize(output), "PNG write failed")
        try json(["path": destination.path, "pid": targetPID, "width": image.width, "height": image.height])
    default: throw Stop(message: "Unsupported operation")
    }
    try await Task.sleep(nanoseconds: 500_000_000)
}
Task { @MainActor in
    do { try await run(); exit(0) }
    catch let stop as Stop { fputs("DEV_UI_STOP: \(stop.message)\n", stderr); exit(1) }
    catch { fputs("DEV_UI_STOP: native operation did not complete; no raw error or credentials logged\n", stderr); exit(1) }
}
dispatchMain()
