import AppKit
import ApplicationServices
let pid = pid_t(CommandLine.arguments[1])!
let app = AXUIElementCreateApplication(pid)
var raw: CFTypeRef?
guard AXUIElementCopyAttributeValue(app, kAXWindowsAttribute as CFString, &raw) == .success,
      let windows = raw as? [AXUIElement] else { fputs("No owned App window\n", stderr); exit(2) }
func area(_ element: AXUIElement) -> Double {
    var value: CFTypeRef?; var size = CGSize.zero
    guard AXUIElementCopyAttributeValue(element, kAXSizeAttribute as CFString, &value) == .success, let value, CFGetTypeID(value) == AXValueGetTypeID() else { return 0 }
    AXValueGetValue(value as! AXValue, .cgSize, &size)
    return size.width * size.height
}
guard let window = windows.max(by: { area($0) < area($1) }) else { fputs("No owned App window\n", stderr); exit(2) }
if CommandLine.arguments.count == 4 {
    if let screen = NSScreen.main {
        var position = CGPoint(x: screen.visibleFrame.minX, y: screen.frame.maxY - screen.visibleFrame.maxY)
        let point = AXValueCreate(.cgPoint, &position)!
        guard AXUIElementSetAttributeValue(window, kAXPositionAttribute as CFString, point) == .success else { fputs("Normal AX positioning unavailable\n", stderr); exit(2) }
    }
    var size = CGSize(width: Double(CommandLine.arguments[2])!, height: Double(CommandLine.arguments[3])!)
    let value = AXValueCreate(.cgSize, &size)!
    guard AXUIElementSetAttributeValue(window, kAXSizeAttribute as CFString, value) == .success else { fputs("Normal AX resize unavailable\n", stderr); exit(2) }
}
let list = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] ?? []
let owned = list.filter { ($0[kCGWindowOwnerPID as String] as? Int32) == pid && ($0[kCGWindowLayer as String] as? Int) == 0 }
let data = try JSONSerialization.data(withJSONObject: owned.map { ["window_id": $0[kCGWindowNumber as String]!, "bounds": $0[kCGWindowBounds as String]!] }, options: [.prettyPrinted, .sortedKeys])
print(String(data: data, encoding: .utf8)!)
