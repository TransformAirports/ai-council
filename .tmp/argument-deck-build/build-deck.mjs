import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = "/Users/christiankessleriv/Repos/ai-council-mwaa";
const OUT = path.join(ROOT, "outputs/stage4");
const REVIEW = path.join(ROOT, ".tmp/argument-deck-build/review");
const PPTX = path.join(OUT, "argument-data-centers-on-aircraft-approach.pptx");

const C = {
  navy: "#0B2D4D",
  blue: "#2E84A5",
  gold: "#D4A24C",
  slate: "#415669",
  white: "#FFFFFF",
  fog: "#EDF3F6",
  green: "#24745C",
  red: "#A6413A",
  ink: "#17232D",
  paleGold: "#F5E9D1",
  lightSlate: "#B7C4CC",
};

const W = 1280;
const H = 720;
const M = 62;

function addShape(slide, geometry, position, fill = "none", lineFill = "none", lineWidth = 0, name) {
  return slide.shapes.add({
    geometry,
    name,
    position,
    fill,
    line: { style: "solid", fill: lineFill, width: lineWidth },
  });
}

function addText(slide, text, position, options = {}) {
  const box = addShape(slide, "textbox", position, options.fill ?? "none", options.lineFill ?? "none", options.lineWidth ?? 0, options.name);
  box.text = text;
  const requestedPt = options.fontSize ?? 18;
  const minimumPt = options.source ? 9 : 16;
  box.text.style = {
    fontFamily: options.fontFamily ?? "Aptos",
    fontSize: Math.max(requestedPt, minimumPt) * (4 / 3),
    bold: options.bold ?? false,
    color: options.color ?? C.ink,
    alignment: options.alignment ?? "left",
    verticalAlignment: options.verticalAlignment ?? "middle",
  };
  return box;
}

function addChrome(slide, section) {
  slide.background.fill = C.white;
  addShape(slide, "line", { left: M, top: 50, width: W - M - 62, height: 0 }, "none", C.lightSlate, 1);
}

function addHeadline(slide, headline, height = 84, fontSize = 38) {
  return addText(slide, headline, { left: M, top: 66, width: 1156, height }, {
    fontFamily: "Georgia", fontSize, bold: true, color: C.navy,
  });
}

function addSource(slide, text) {
  addShape(slide, "line", { left: M, top: 674, width: 1156, height: 0 }, "none", C.lightSlate, 1);
  addText(slide, text, { left: M, top: 680, width: 1156, height: 24 }, {
    fontSize: 9, color: C.slate, alignment: "center", source: true,
  });
}

function setNotes(slide, talkTrack, urls) {
  slide.speakerNotes.textFrame.setText(`${talkTrack}\n\n[Sources]\n${urls.map((u) => `- ${u}`).join("\n")}\n[/Sources]`);
  slide.speakerNotes.setVisible(true);
}

function buildSlide1(presentation) {
  const slide = presentation.slides.add();
  addChrome(slide, "01  /  IRREVERSIBILITY");
  addHeadline(slide, "This ground is reserved capacity. A data center pours the option in concrete.", 104, 44);

  const y = 333;
  const xs = [112, 350, 588, 826, 1064];
  addShape(slide, "line", { left: xs[0], top: y, width: xs[4] - xs[0], height: 0 }, "none", C.navy, 5);
  const years = ["1958", "1985", "2005", "2024", "2025"];
  const labels = [
    "Fifth runway enters\nDulles designs",
    "Capacity carried in\nthe master plan",
    "FAA approves fourth\nand fifth runways",
    "27.25M passengers;\nUnited ≈70% of flights",
    "Board reaffirms path\ntoward ≈90M passengers",
  ];
  xs.forEach((x, i) => {
    addShape(slide, "ellipse", { left: x - 13, top: y - 13, width: 26, height: 26 }, i === 4 ? C.gold : C.white, C.navy, 4);
    addText(slide, years[i], { left: x - 58, top: y - 72, width: 116, height: 34 }, {
      fontFamily: "Georgia", fontSize: 24, bold: true, color: i === 4 ? C.gold : C.navy, alignment: "center",
    });
    addText(slide, labels[i], { left: x - 88, top: y + 32, width: 176, height: 74 }, {
      fontSize: 16, color: C.ink, alignment: "center",
    });
  });

  addShape(slide, "rect", { left: 72, top: 500, width: 1136, height: 104 }, C.fog, "none", 0);
  addShape(slide, "rect", { left: 72, top: 500, width: 8, height: 104 }, C.gold, "none", 0);
  addText(slide, "The parcel sits inside the RWY 1L approach and RWY 19R departure surfaces of a growing airfield.", { left: 100, top: 518, width: 1082, height: 66 }, {
    fontFamily: "Georgia", fontSize: 25, bold: true, color: C.navy, alignment: "center",
  });
  addSource(slide, "Sources: MWAA master-plan update (2025); FAA Record of Decision (2005); FFXnow passenger record; Simple Flying market-share analysis.");
  setNotes(slide,
    "Lead with irreversibility, not the hazard list. Each hazard can be evaluated and conditioned. The permanent commitment of reserved capacity land cannot. Avoid claiming that the parcel lies on the published fifth-runway alignment; the relevant claim is the 1L/19R protected surfaces and extension capacity.",
    [
      "https://www.mwaa.com/news/dulles-master-plan-update-sets-framework-decades-airport-development",
      "https://www.ffxnow.com/2025/07/17/new-master-plan-for-dulles-airport-envisions-growth-to-90-million-annual-passengers/",
      "https://www.flydulles.com/d2-projects-future-fifth-runway",
    ],
  );
}

function buildSlide2(presentation) {
  const slide = presentation.slides.add();
  addChrome(slide, "02  /  SIGNATURE VISUAL");
  addHeadline(slide, "The law leaves 25 to 200 feet of air above this parcel.", 112, 35);

  const left = 110;
  const right = 1110;
  const ground = 510;
  const plotTop = 230;
  const plotW = right - left;
  const plotH = ground - plotTop;
  const x = (ft) => left + (ft / 4000) * plotW;
  const y = (ft) => ground - (ft / 250) * plotH;

  for (let ft = 0; ft <= 250; ft += 50) {
    addShape(slide, "line", { left, top: y(ft), width: plotW, height: 0 }, "none", ft === 0 ? C.navy : C.fog, ft === 0 ? 3 : 1);
  }
  for (let ft = 0; ft <= 4000; ft += 1000) {
    addShape(slide, "line", { left: x(ft), top: ground, width: 0, height: 8 }, "none", C.navy, 2);
    addText(slide, ft === 0 ? "RWY END" : `${ft.toLocaleString()} ft`, { left: x(ft) - 65, top: ground + 12, width: 130, height: 28 }, { fontSize: 11, bold: ft === 0, color: C.slate, alignment: "center" });
  }
  addText(slide, "0–250 FT AGL", { left: 110, top: 202, width: 180, height: 24 }, { fontSize: 16, bold: true, color: C.slate });

  addShape(slide, "line", { left: x(0), top: y(80), width: x(4000) - x(0), height: y(0) - y(80), verticalFlip: true }, "none", C.blue, 4);
  addText(slide, "50:1 APPROACH", { left: 790, top: y(67) - 26, width: 230, height: 28 }, { fontSize: 16, bold: true, color: C.blue });
  addShape(slide, "line", { left: x(0), top: y(100), width: x(4000) - x(0), height: y(0) - y(100), verticalFlip: true }, "none", C.slate, 3);
  addText(slide, "40:1 DEPARTURE", { left: 850, top: y(94) - 30, width: 250, height: 28 }, { fontSize: 16, bold: true, color: C.slate });
  addShape(slide, "line", { left: x(0), top: y(239), width: x(3600) - x(0), height: y(50) - y(239), verticalFlip: true }, "none", C.gold, 5);
  addText(slide, "3° GLIDEPATH", { left: 1010, top: 300, width: 180, height: 28 }, { fontSize: 16, bold: true, color: C.gold });

  const hallX = x(2500) - 52;
  addShape(slide, "rect", { left: hallX, top: y(50), width: 104, height: ground - y(50) }, C.red, C.red, 1, "SIGNATURE VISUAL — generic 50-foot data hall");
  addShape(slide, "rect", { left: hallX + 13, top: y(50) - 10, width: 22, height: 10 }, C.red, "none", 0);
  addShape(slide, "rect", { left: hallX + 69, top: y(50) - 15, width: 14, height: 15 }, C.red, "none", 0);
  addText(slide, "50-FT\nHALL", { left: hallX + 8, top: y(50) + 2, width: 88, height: 50 }, { fontSize: 16, bold: true, color: C.white, alignment: "center" });

  [1000, 2000, 3000].forEach((ft, i) => {
    const alt = [102, 155, 207][i];
    addShape(slide, "ellipse", { left: x(ft) - 7, top: y(alt) - 7, width: 14, height: 14 }, C.gold, C.white, 2);
    addText(slide, `≈${alt} ft`, { left: x(ft) - 55, top: y(alt) - 38, width: 110, height: 30 }, { fontSize: 14, bold: true, color: C.gold, alignment: "center" });
  });

  addShape(slide, "line", { left: x(0), top: ground - 9, width: x(2400) - x(0), height: 0 }, "none", C.green, 5);
  for (let ft = 0; ft <= 2400; ft += 400) addShape(slide, "line", { left: x(ft), top: ground - 18, width: 0, height: 18 }, "none", C.green, 2);
  addText(slide, "ALSF-2  ·  2,400 FT", { left: x(700), top: ground - 44, width: 260, height: 24 }, { fontSize: 14, bold: true, color: C.green, alignment: "center" });

  addText(slide, "50-ft object meets 50:1 surface at ≈2,500 ft", { left: 400, top: 202, width: 430, height: 26 }, { fontSize: 16, bold: true, color: C.red, alignment: "center" });
  addText(slide, "25 ft allowable at 1,000 ft on the 40:1 surface", { left: 112, top: 566, width: 430, height: 52 }, { fontSize: 16, bold: true, color: C.slate });

  addShape(slide, "rect", { left: 822, top: 574, width: 386, height: 82 }, C.fog, "none", 0);
  addText(slide, "WILDLIFE SEPARATION  /  10,000 FT", { left: 840, top: 580, width: 350, height: 28 }, { fontSize: 16, bold: true, color: C.slate, alignment: "center" });
  addShape(slide, "line", { left: 842, top: 632, width: 330, height: 0 }, "none", C.navy, 3);
  addShape(slide, "ellipse", { left: 901, top: 621, width: 22, height: 22 }, C.blue, C.white, 2);
  addText(slide, "pond", { left: 932, top: 611, width: 100, height: 36 }, { fontSize: 16, bold: true, color: C.blue });

  addText(slide, "FAA HEIGHT  /  1–4K FT", { left: 570, top: 574, width: 230, height: 28 }, { fontSize: 16, bold: true, color: C.slate, alignment: "center" });
  slide.charts.add("line", {
    position: { left: 570, top: 602, width: 230, height: 54 },
    categories: ["1", "2", "3", "4"],
    series: [
      { name: "50:1 approach", values: [20, 40, 60, 80], line: { style: "solid", fill: C.blue, width: 3 }, marker: { symbol: "none" } },
      { name: "40:1 departure", values: [25, 50, 75, 100], line: { style: "solid", fill: C.slate, width: 3 }, marker: { symbol: "none" } },
    ],
    hasLegend: false,
    lineOptions: { grouping: "standard", smooth: false },
    xAxis: { visible: false, majorGridlines: null },
    yAxis: { visible: false, min: 0, max: 100, majorGridlines: null },
    chartFill: "none",
    chartLine: { style: "solid", fill: "none", width: 0 },
    plotAreaFill: "none",
    plotAreaLine: { style: "solid", fill: "none", width: 0 },
  });

  addText(slide, "Notes: flat terrain at runway-end elevation; generic massing; published FAA geometry, not the unpublished site plan.", { left: 62, top: 650, width: 734, height: 20 }, { fontSize: 9, color: C.slate, source: true });
  addSource(slide, "Sources: 14 CFR 77.19; FAA AC 150/5300-13B; FAA ALSF-2 specifications; FAA AC 150/5200-33C; analyst geometry.");
  setNotes(slide,
    "This is the mechanism slide. The correct claim is the geometry, not a proven upset. The published surfaces leave little vertical margin for a generic 50-foot hall and rooftop plant. FAA plume guidance rates overall disruption risk low for transport-category jets; do not claim that plume will endanger heavy aircraft.",
    [
      "https://www.ecfr.gov/current/title-14/chapter-I/subchapter-E/part-77/subpart-C/section-77.19",
      "https://www.faa.gov/airports/resources/advisory_circulars/",
      "https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/lsg/als",
      "https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf",
    ],
  );
}

function buildSlide3(presentation) {
  const slide = presentation.slides.add();
  addChrome(slide, "03  /  COUNTER-CASE");
  addHeadline(slide, "The 2018 sale protected capacity first. This proposal reverses the order.", 118, 35);

  addText(slide, "THE COUNTER-CASE, AT FULL STRENGTH", { left: 72, top: 224, width: 500, height: 58 }, { fontSize: 18, bold: true, color: C.slate });
  addShape(slide, "line", { left: 614, top: 224, width: 0, height: 406 }, "none", C.lightSlate, 2);
  const counter = [
    ["$236.5M", "424 acres · ≈$558K per acre"],
    ["≈70%", "Estimated global internet traffic through Ashburn"],
    ["GA 24", "Airport should be self-sustaining"],
    ["LOW", "FAA overall plume disruption risk"],
  ];
  counter.forEach(([metric, copy], i) => {
    const top = 294 + i * 72;
    addText(slide, metric, { left: 74, top, width: 180, height: 48 }, { fontFamily: "Georgia", fontSize: 24, bold: true, color: C.blue });
    addText(slide, copy, { left: 270, top: top - 2, width: 292, height: 54 }, { fontSize: 16, color: C.ink });
  });

  addText(slide, "THE ANSWER, FROM THE SAME RECORD", { left: 660, top: 224, width: 520, height: 44 }, { fontSize: 18, bold: true, color: C.navy });
  addText(slide, "2018 DISCIPLINE", { left: 660, top: 292, width: 220, height: 30 }, { fontSize: 16, bold: true, color: C.slate });
  const s1 = addShape(slide, "roundRect", { left: 660, top: 328, width: 220, height: 86 }, C.fog, C.blue, 2);
  addText(slide, "Build runway +\nsupport area", { left: 675, top: 340, width: 190, height: 62 }, { fontSize: 16, bold: true, color: C.navy, alignment: "center" });
  const s2 = addShape(slide, "roundRect", { left: 962, top: 328, width: 220, height: 86 }, C.fog, C.blue, 2);
  addText(slide, "Sell remaining\nsurplus", { left: 977, top: 340, width: 190, height: 62 }, { fontSize: 16, bold: true, color: C.navy, alignment: "center" });
  slide.shapes.connect(s1, s2, { kind: "straight", fromSide: "right", toSide: "left", line: { style: "solid", fill: C.blue, width: 3 }, tail: { type: "triangle", width: "med", length: "med" } });

  addText(slide, "CURRENT PROPOSAL", { left: 660, top: 438, width: 220, height: 30 }, { fontSize: 16, bold: true, color: C.red });
  const s3 = addShape(slide, "roundRect", { left: 660, top: 474, width: 220, height: 86 }, C.paleGold, C.red, 3);
  addText(slide, "Sell reserved\ncapacity", { left: 675, top: 486, width: 190, height: 62 }, { fontSize: 16, bold: true, color: C.red, alignment: "center" });
  const s4 = addShape(slide, "roundRect", { left: 962, top: 474, width: 220, height: 86 }, C.paleGold, C.red, 3);
  addText(slide, "Foreclose the\n1L/19R option", { left: 977, top: 486, width: 190, height: 62 }, { fontSize: 16, bold: true, color: C.red, alignment: "center" });
  slide.shapes.connect(s3, s4, { kind: "straight", fromSide: "right", toSide: "left", line: { style: "solid", fill: C.red, width: 3 }, tail: { type: "triangle", width: "med", length: "med" } });

  addShape(slide, "rect", { left: 650, top: 584, width: 548, height: 66 }, C.navy, "none", 0);
  addText(slide, "Condition every hazard. You still cannot reverse a land commitment.", { left: 675, top: 594, width: 498, height: 46 }, { fontFamily: "Georgia", fontSize: 18, bold: true, color: C.white, alignment: "center" });
  addSource(slide, "Sources: MWAA Western Lands sale; Lightyear Data Center Alley guide; FAA Grant Assurance 24; FAA thermal-plume guidance.");
  setNotes(slide,
    "Do not caricature the opposition. Concede the verified revenue, connectivity, self-sustainability, and plume points. Then use the 2018 sale as the governing rule: MWAA protected capacity first and sold only the surplus remaining after the fourth runway and support area were built.",
    [
      "https://www.mwaa.com/news/airports-authority-announces-sale-424-acres-western-lands-dulles-international",
      "https://lightyear.ai/blogs/ashburn-colocation-data-center-alley",
      "https://www.faa.gov/airports/aip/grant_assurances/assurances-airport-sponsors-2025",
      "https://www.faa.gov/sites/faa.gov/files/airports/environmental/land_use/Technical-Guidance-Assessment-Tool-Thermal-Exhaust-Plume-Impact.pdf",
    ],
  );
}

function buildSlide4(presentation) {
  const slide = presentation.slides.add();
  addChrome(slide, "04  /  THE ASK");
  addHeadline(slide, "The ask: the gate, not a slogan — sell the surplus, keep the runway.", 126, 35);

  const steps = [
    ["1", "NO APPROVAL", "Do not approve from a circulated project email."],
    ["2", "FAA REVIEW", "ADO coordination + Form 7460-1 evaluation."],
    ["3", "TECHNICAL PROOF", "Glare, plume, EMI + wildlife-safe stormwater."],
    ["4", "FORMAL PLAN", "ALP amendment consistent with the master plan."],
    ["5", "REJECT THIS SITE", "No study cures foreclosure of reserved capacity."],
  ];
  const startX = 72;
  const gap = 14;
  const sw = 216;
  steps.forEach(([num, label, copy], i) => {
    const sx = startX + i * (sw + gap);
    const final = i === 4;
    addShape(slide, "rect", { left: sx, top: 210, width: sw, height: 204 }, final ? C.navy : C.fog, final ? C.navy : C.lightSlate, final ? 0 : 1);
    addText(slide, num, { left: sx + 15, top: 222, width: 42, height: 40 }, { fontFamily: "Georgia", fontSize: 27, bold: true, color: final ? C.gold : C.blue });
    addText(slide, label, { left: sx + 15, top: 268, width: sw - 30, height: 50 }, { fontSize: 16, bold: true, color: final ? C.white : C.navy });
    addText(slide, copy, { left: sx + 15, top: 324, width: sw - 30, height: 78 }, { fontSize: 16, bold: final, color: final ? C.white : C.ink });
    if (i < 4) addText(slide, "→", { left: sx + sw - 3, top: 286, width: gap + 6, height: 34 }, { fontSize: 25, bold: true, color: C.gold, alignment: "center" });
  });

  addText(slide, "ARGUE ON THE FAA'S OWN STANDARD", { left: 72, top: 432, width: 520, height: 40 }, { fontSize: 18, bold: true, color: C.navy });
  addText(slide, "SECTION 163  ·  CONFIRM WITH COUNSEL", { left: 720, top: 432, width: 488, height: 40 }, { fontSize: 16, bold: true, color: C.slate, alignment: "right" });
  addShape(slide, "rect", { left: 72, top: 476, width: 1136, height: 136 }, C.white, C.navy, 2);
  const tests = [
    ["A", "Materially affects safe, efficient aircraft operation"],
    ["B", "Endangers people or property on the ground"],
    ["C", "Diminishes prior federal investment"],
  ];
  tests.forEach(([letter, copy], i) => {
    const tx = 95 + i * 367;
    addShape(slide, "ellipse", { left: tx, top: 500, width: 48, height: 48 }, i === 2 ? C.gold : C.navy, "none", 0);
    addText(slide, letter, { left: tx, top: 500, width: 48, height: 48 }, { fontFamily: "Georgia", fontSize: 23, bold: true, color: C.white, alignment: "center" });
    addText(slide, copy, { left: tx + 62, top: 488, width: 270, height: 72 }, { fontSize: 16, bold: true, color: C.ink });
    if (i === 2) addText(slide, "≈$64M in two 2026 grants", { left: tx + 62, top: 558, width: 270, height: 36 }, { fontSize: 16, bold: true, color: C.gold });
  });
  addText(slide, "Grant Assurances 19–22 and 29 bind MWAA. The federal lease runs to 2100.", { left: 72, top: 626, width: 1136, height: 34 }, { fontFamily: "Georgia", fontSize: 19, bold: true, color: C.navy, alignment: "center" });
  addSource(slide, "Sources: 14 CFR Part 77; FAA Sponsor Assurances; 49 U.S.C. 47107; Section 163; FY2026 grants; MWAA federal lease.");
  setNotes(slide,
    "The recommendation is a gate and a siting decision. Require every FAA study and formal plan action, then reject this location because no favorable study can cure the irreversible commitment of reserved capacity. Section 163 was revised in 2024; counsel should confirm the current framework before a formal submission.",
    [
      "https://www.ecfr.gov/current/title-14/chapter-I/subchapter-E/part-77",
      "https://www.faa.gov/sites/faa.gov/files/airports/aip/grant_assurances/airport-sponsor-assurances-aip.pdf",
      "https://www.federalregister.gov/documents/2023/12/08/2023-27017/policy-regarding-processing-land-use-changes-on-federally-acquired-or-federally-conveyed-airport",
      "https://www.ffxnow.com/2026/05/20/dulles-airport-lands-41m-federal-grant-for-concourse-e-construction/",
      "https://www.mwaa.com/news/secretary-transportation-and-airports-authority-sign-lease-extension-operation-washingtons",
    ],
  );
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

async function main() {
  await fs.mkdir(OUT, { recursive: true });
  await fs.rm(REVIEW, { recursive: true, force: true });
  await fs.mkdir(REVIEW, { recursive: true });
  const presentation = Presentation.create({ slideSize: { width: W, height: H } });
  buildSlide1(presentation);
  buildSlide2(presentation);
  buildSlide3(presentation);
  buildSlide4(presentation);

  for (const [index, slide] of presentation.slides.items.entries()) {
    const stem = `slide-${String(index + 1).padStart(2, "0")}`;
    await writeBlob(path.join(REVIEW, `${stem}.png`), await presentation.export({ slide, format: "png", scale: 1.5 }));
    const layout = await slide.export({ format: "layout" });
    await fs.writeFile(path.join(REVIEW, `${stem}.layout.json`), await layout.text());
  }
  await writeBlob(path.join(REVIEW, "montage.webp"), await presentation.export({ format: "webp", montage: true, scale: 1 }));
  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(PPTX);
  console.log(JSON.stringify({ pptx: PPTX, slides: presentation.slides.items.length, review: REVIEW }));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
