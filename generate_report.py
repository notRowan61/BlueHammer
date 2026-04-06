#!/usr/bin/env python3
"""Generate a PDF report analyzing the BlueHammer repository."""

from fpdf import FPDF


class Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "BlueHammer Repository Analysis", align="R")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 60, 120)
        self.cell(0, 10, title)
        self.ln(8)
        self.set_draw_color(30, 60, 120)
        self.line(self.get_x(), self.get_y(), self.get_x() + 180, self.get_y())
        self.ln(6)

    def subsection_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title)
        self.ln(6)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def table_row(self, col1, col2, bold=False):
        style = "B" if bold else ""
        self.set_font("Helvetica", style, 9)
        if bold:
            self.set_fill_color(30, 60, 120)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(245, 245, 250)
            self.set_text_color(40, 40, 40)
        self.cell(55, 7, col1, border=1, fill=True)
        self.cell(125, 7, col2, border=1, fill=True)
        self.ln()


pdf = Report()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Title page content
pdf.set_font("Helvetica", "B", 28)
pdf.set_text_color(30, 60, 120)
pdf.ln(40)
pdf.cell(0, 15, "BlueHammer", align="C")
pdf.ln(14)
pdf.set_font("Helvetica", "", 16)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 10, "Repository Analysis Report", align="C")
pdf.ln(20)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "Generated: April 6, 2026", align="C")
pdf.ln(6)
pdf.cell(0, 8, "Repository: manueltarouca/BlueHammer", align="C")
pdf.ln(6)
pdf.cell(0, 8, "License: MIT (Copyright 2026 Nightmare-Eclipse)", align="C")

# Page 2 - Overview
pdf.add_page()
pdf.section_title("1. Project Overview")
pdf.body_text(
    "BlueHammer is a proof-of-concept (PoC) Windows privilege escalation exploit "
    "written in C++. It demonstrates the \"BlueHammer vulnerability\" -- a technique "
    "to leak protected system files such as the SAM database, which contains Windows "
    "user password hashes."
)
pdf.body_text(
    "The vulnerability was originally disclosed by Tom Gallagher, Igor Tsyganskiy, "
    "and Jeremy Tinder. The README notes that the PoC contains some bugs and may not "
    "work as-is."
)

pdf.section_title("2. Technology Stack")
pdf.table_row("Category", "Details", bold=True)
pdf.table_row("Language", "C++ (with C for auto-generated stubs)")
pdf.table_row("Build System", "Visual Studio 2022 (v143 platform toolset)")
pdf.table_row("Target Platform", "Windows 10+ (x64 and Win32)")
pdf.table_row("Character Set", "Unicode")
pdf.table_row("Key Libraries", "Offline Registry (OReg), Windows RPC/ALPC")
pdf.ln(5)

# Page 3 - Project Structure
pdf.section_title("3. Project Structure")
pdf.table_row("File", "Purpose", bold=True)
pdf.table_row("FunnyApp.cpp (~3,450 lines)", "Main exploit logic - core of the project")
pdf.table_row("FunnyApp.sln / .vcxproj", "Visual Studio solution & project files")
pdf.table_row("windefend.idl (2,412 lines)", "Windows Defender RPC interface definition")
pdf.table_row("windefend_c.c (~73K lines)", "Auto-generated RPC client stubs")
pdf.table_row("windefend_s.c (~68K lines)", "Auto-generated RPC server stubs")
pdf.table_row("windefend_h.h (2,586 lines)", "Generated RPC header file")
pdf.table_row("offreg.h / offreg.lib", "Microsoft Offline Registry API")
pdf.table_row("FunnyApp.rc / resource.h", "Resource script and definitions")
pdf.table_row("FunnyApp.aps", "AppStudio resource file")
pdf.table_row("x64/Release/FunnyApp.exe", "Compiled 64-bit release executable")
pdf.ln(5)
pdf.body_text(
    "The codebase totals approximately 147,700 lines, but the vast majority (~141K lines) "
    "consists of auto-generated RPC stubs. The actual exploit logic resides entirely in "
    "FunnyApp.cpp at roughly 3,450 lines."
)

# Page 4 - Windows APIs Used
pdf.add_page()
pdf.section_title("4. Windows APIs and Subsystems Used")

pdf.subsection_title("Core Windows APIs")
pdf.bullet("Kernel32 / Ntdll - Low-level NT system calls and file operations")
pdf.bullet("NT Object Manager - NtCreateSymbolicLinkObject, NtOpenDirectoryObject")
pdf.bullet("Security/Token Management - Privilege escalation and impersonation")

pdf.subsection_title("Specialized Subsystems")
pdf.bullet("RPC/ALPC - Communication with Windows Defender service")
pdf.bullet("Volume Shadow Copy Service (VSS) - Accessing protected system files")
pdf.bullet("Cloud Filter API (CldApi) - Placeholder/callback-based file interception")
pdf.bullet("Windows Update API (WuApi) - Monitoring update cycles")
pdf.bullet("Cabinet API (FDI) - Handling .cab archive files")
pdf.bullet("SDDL / Security APIs - Security descriptor manipulation")
pdf.bullet("Offline Registry (OReg) - Direct registry hive file manipulation")
pdf.bullet("Cryptographic APIs - Hash computation (SHA-256, NTLMv2)")

# Page 5 - Exploit Flow
pdf.section_title("5. Exploit Attack Chain")
pdf.body_text(
    "The exploit entry point is wmain() at FunnyApp.cpp:2881. It orchestrates a "
    "multi-stage attack with approximately 55 helper functions. The stages are:"
)

pdf.subsection_title("Stage 1: Monitor Windows Defender Updates")
pdf.body_text(
    "The exploit monitors Windows Defender definition update directories, waiting for "
    "an update cycle to begin. This provides a timing window for the attack."
)

pdf.subsection_title("Stage 2: Volume Shadow Copy Manipulation")
pdf.body_text(
    "Leverages the Volume Shadow Copy Service (VSS) to access protected system files "
    "such as C:\\Windows\\System32\\Config\\SAM (password database) and SYSTEM/SECURITY "
    "registry hives."
)

pdf.subsection_title("Stage 3: Symbolic Links and Junctions")
pdf.body_text(
    "Creates NT object manager symbolic links and filesystem junctions to redirect "
    "file system access, causing privileged processes to read/write attacker-controlled "
    "locations."
)

pdf.subsection_title("Stage 4: Oplock Race Conditions")
pdf.body_text(
    "Sets opportunistic locks (oplocks) on target files and exploits the resulting "
    "race condition during file move operations to intercept and redirect I/O."
)

pdf.add_page()
pdf.subsection_title("Stage 5: Windows Defender RPC Coordination")
pdf.body_text(
    "Makes RPC calls to Windows Defender via ServerMpUpdateEngineSignature to "
    "coordinate attack timing and trigger specific Defender behaviors."
)

pdf.subsection_title("Stage 6: Sensitive Data Extraction")
pdf.body_text(
    "Extracts and decrypts LSA secrets and NTLM password hashes from the obtained "
    "registry hive data using offline registry manipulation and cryptographic routines."
)

pdf.subsection_title("Stage 7: Credential Modification (Optional)")
pdf.body_text(
    "Can compute new NT hashes and modify user passwords by writing directly to the "
    "SAM database, bypassing normal authentication controls."
)

pdf.subsection_title("Stage 8: Privileged Shell Spawning")
pdf.body_text(
    "If running as SYSTEM, can launch interactive consoles in any user session via "
    "LaunchConsoleInSessionId() and DoSpawnShellAsAllUsers()."
)

# Key Functions
pdf.section_title("6. Key Functions")
pdf.table_row("Function", "Role", bold=True)
pdf.table_row("wmain()", "Entry point; orchestrates the exploit")
pdf.table_row("IsRunningAsLocalSystem()", "Checks for SYSTEM-level privileges")
pdf.table_row("LaunchConsoleInSessionId()", "Spawns interactive console in session")
pdf.table_row("CallWD() / WDCallerThread()", "RPC calls to Windows Defender")
pdf.table_row("CheckForWDUpdates()", "Monitors Defender definition updates")
pdf.table_row("ShadowCopyFinderThread()", "Locates Volume Shadow Copy data")
pdf.table_row("GetWDPID()", "Retrieves Windows Defender process ID")
pdf.table_row("CfCallbackFetchPlaceHolders()", "Cloud Filter callback for interception")
pdf.table_row("FreezeVSS()", "Freezes Volume Shadow Copy state")
pdf.table_row("TriggerWDForVS()", "Triggers WD for VSS interaction")
pdf.table_row("GetLSASecretKey()", "Extracts LSA secret decryption key")
pdf.table_row("ComputeSHA256()", "SHA-256 hash computation")
pdf.table_row("ChangeUserPassword()", "Modifies passwords via NTLMv2 hash")
pdf.table_row("DoSpawnShellAsAllUsers()", "Spawns shells with various privileges")

# Summary
pdf.add_page()
pdf.section_title("7. Summary and Notes")
pdf.body_text(
    "BlueHammer is a sophisticated Windows privilege escalation PoC that chains "
    "multiple attack primitives -- VSS abuse, symbolic link attacks, oplock races, "
    "and RPC manipulation -- to extract protected credential data from a Windows system."
)
pdf.body_text(
    "The project is structured as a single Visual Studio solution with one main source "
    "file (FunnyApp.cpp) supported by auto-generated Windows Defender RPC interface "
    "stubs. The exploit requires deep knowledge of Windows internals including the NT "
    "object namespace, file system filter drivers, and the Volume Shadow Copy Service."
)
pdf.body_text(
    "Key considerations:"
)
pdf.bullet("The PoC has known bugs and may not function correctly as-is")
pdf.bullet("Licensed under MIT by Nightmare-Eclipse (2026)")
pdf.bullet("Credits Tom Gallagher, Igor Tsyganskiy, and Jeremy Tinder for disclosure")
pdf.bullet("Targets Windows 10+ systems (x64 architecture)")
pdf.bullet("The compiled executable is included at x64/Release/FunnyApp.exe")

output_path = "/home/user/BlueHammer/BlueHammer_Analysis_Report.pdf"
pdf.output(output_path)
print(f"PDF report saved to: {output_path}")
