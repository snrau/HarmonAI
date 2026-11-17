<script>
    import {
        music,
        process_harmonizations_for_visualization,
        smallest_duration_considered,
        selectedIndex,
        selectedKey,
    } from "../state.svelte.js";

    import { onMount } from "svelte";

    import { playHarmonization } from "../helper/musicutil.js";

    import * as LineUpJS from "lineupjs";
    import * as d3 from "d3";
    import "../../node_modules/lineupjs/build/LineUpJS.css";
    import { getSingleRowMetrics } from "../helper/servercomms.js";
    import {
        cyclicHarmonicColoring,
        cyclicKeyMode,
    } from "../helper/coloring.js";

    let container;
    //let container2;

    let lineUp;

    let observer;

    const KEYS = [
        { label: "C major", name: "C major", color: cyclicKeyMode(0) },
        { label: "a minor", name: "a minor", color: cyclicKeyMode(0, false) },

        { label: "G major", name: "G major", color: cyclicKeyMode(7) },
        { label: "e minor", name: "e minor", color: cyclicKeyMode(7, false) },

        { label: "D major", name: "D major", color: cyclicKeyMode(2) },
        { label: "b minor", name: "b minor", color: cyclicKeyMode(2, false) },

        { label: "A major", name: "A major", color: cyclicKeyMode(9) },
        { label: "f# minor", name: "f# minor", color: cyclicKeyMode(9, false) },

        { label: "E major", name: "E major", color: cyclicKeyMode(4) },
        { label: "c# minor", name: "c# minor", color: cyclicKeyMode(4, false) },

        { label: "B major", name: "B major", color: cyclicKeyMode(11) },
        {
            label: "g# minor",
            name: "g# minor",
            color: cyclicKeyMode(11, false),
        },

        { label: "F# major", name: "F# major", color: cyclicKeyMode(6) },
        { label: "d# minor", name: "d# minor", color: cyclicKeyMode(6, false) },
        { label: "G- major", name: "G- major", color: cyclicKeyMode(6) },
        { label: "e- minor", name: "e- minor", color: cyclicKeyMode(6, false) },

        { label: "D- major", name: "D- major", color: cyclicKeyMode(1) },
        { label: "b- minor", name: "b- minor", color: cyclicKeyMode(1, false) },

        { label: "A- major", name: "A- major", color: cyclicKeyMode(8) },
        { label: "f minor", name: "f minor", color: cyclicKeyMode(8, false) },

        { label: "E- major", name: "E- major", color: cyclicKeyMode(3) },
        { label: "c minor", name: "c minor", color: cyclicKeyMode(3, false) },

        { label: "B- major", name: "B- major", color: cyclicKeyMode(10) },
        { label: "g minor", name: "g minor", color: cyclicKeyMode(10, false) },

        { label: "F major", name: "F major", color: cyclicKeyMode(5) },
        { label: "d minor", name: "d minor", color: cyclicKeyMode(5, false) },
    ];

    const keyColorMapping = Object.fromEntries(
        KEYS.map((k) => [k.name, k.color]),
    );

    onMount(() => {
        observer = new MutationObserver(checkForKeyHeader);

        observer.observe(container, {
            childList: true,
            subtree: true,
        });
    });

    function checkForKeyHeader() {
        if (container) {
            processed.forEach((_, row) => {
                const selector = "col" + (row + 1);
                const spacingDiv = container.querySelector(
                    'article[data-ranking="rank0"] div[data-i="' +
                        row +
                        '"] div[data-id="col1"] .lu-cat-label', //'section[title="Key"] .lu-spacing',
                );

                if (spacingDiv && !spacingDiv.querySelector("#key-select")) {
                    addSelectionToLineUp(spacingDiv, row);

                    // optional: stop observer after adding
                    //observer.disconnect();
                }
            });
        }
    }

    const processed = $derived.by(() => {
        return process_harmonizations_for_visualization(music.harmonizations);
    });

    /*
    $effect(() => {
        const idx = $selectedIndex;
        if (idx >= 0 && music.harmonizations[idx]) {
            // Set selectedKey to the key of the selected harmonization
            selectedKey.set(music.harmonizations[idx].key);
        } else {
            // No selection
            selectedKey.set("");
        }
        const select = container?.querySelector("#key-select");
        if (select && select.value !== $selectedKey) {
            select.value = $selectedKey;
        }
    });
    */

    function updateKey(event, idx) {
        const newKey = event.target.value;
        if (idx === -1) return;

        getSingleRowMetrics(idx, newKey);

        const colorDiv = container.querySelector(
            'article[data-ranking="rank0"] div[data-i="' +
                idx +
                '"] div[data-id="col1"] .lu-cat-color', //'section[title="Key"] .lu-spacing',
        );

        colorDiv.style.backgroundColor =
            KEYS.find((k) => k.name === newKey)?.color || "transparent";

        recolorKeyDistribution();

        /*
        // Update the original harmonization
        music.harmonizations[$selectedIndex].key = newKey;

        // Update the processed data for LineUp
        processed[$selectedIndex].key = newKey;

        */

        // Trigger LineUp rerender
        //lineUp.data.setData(processed);
    }

    $effect(() => {
        if (music.harmonizations.length > 0) {
            //change of innerHTML needs to come before adding lineup for some reason
            document.getElementById("lineup").innerHTML = "";
            //document.getElementById("lineup2").innerHTML = "";

            // give the user a default view that is tailored to the data
            // lineup allows the user anyway to modify the representation
            //const lineup2 = LineUpJS.asTaggle(container2, process_harmonizations_for_lineUp(music.harmonizations));
            const builder = LineUpJS.builder(processed);

            // prepare for and manually define columns
            let piece_duration =
                music.harmonizations[0]["chord_starting_times"][
                    music.harmonizations[0]["chord_starting_times"].length - 1
                ] +
                music.harmonizations[0]["chord_durations"][
                    music.harmonizations[0]["chord_durations"].length - 1
                ];
            let total_number_of_timestamps =
                piece_duration / smallest_duration_considered;
            let timestamps = Array(total_number_of_timestamps);
            for (let i = 0; i < timestamps.length; i++) {
                timestamps[i] =
                    i * smallest_duration_considered +
                    " Quarter notes from beginning";
            }

            const binary_color = (v) => (v === 1 ? "darkcyan" : "#aaa");

            const noteColor = (v) => {
                console.log(v);
                return "darkblue";
            };

            const width_single_value = 40;
            const width_progression = 200;

            builder
                .column(
                    LineUpJS.buildNumberColumn(
                        "typicality_of_chords_per_chord",
                        [0, 1],
                    )
                        .width(width_progression)
                        .label("Typical chord transition indication per chord")
                        .colorMapping(binary_color)
                        .asArray(timestamps)
                        .renderer("heatmap")
                        .htmlSummary(
                            "either 0 or 1<br>0 = not part of a typical chord progression<br>1 = part of a typical chord progression",
                        ),
                )
                .column(
                    LineUpJS.buildCategoricalColumn("roman_numerals")
                        .width(width_single_value)
                        .label("Roman Numerals (String)")
                        .renderer("string", "default", "categorical")
                        .asArray(timestamps),
                )
                .column(
                    LineUpJS.buildCategoricalColumn(
                        "roman_numerals_reflecting_durations",
                    )
                        .width(width_progression)
                        .label("Roman Numerals")
                        .renderer(
                            "catheatmap",
                            "catheatmap",
                            "catdistributionbar",
                        )
                        .asArray(timestamps),
                )
                .column(
                    LineUpJS.buildNumberColumn(
                        "typical_chord_progression_coverage",
                        [0, 100],
                    )
                        .width(width_single_value)
                        .label("Typicality Percentage")
                        .colorMapping(
                            d3.scaleLinear([0, 1], ["#aaa", "darkcyan"]),
                        )
                        .numberFormat(d3.format("d"))
                        .renderer("number", "default", "violin")
                        .htmlSummary(
                            "0 = no typical transition; 100% = entirely consisting of typical transitions",
                        ),
                )
                .column(
                    LineUpJS.buildNumberColumn(
                        "chords_bass_note_midi_reflecting_durations",
                    )
                        .width(width_progression)
                        .renderer("sparkline")
                        .label("Bass Tones (midi)")
                        .asArray(timestamps),
                )
                .column(
                    LineUpJS.buildNumberColumn(
                        "chord_durations_reflecting_durations",
                    )
                        .width(width_progression)
                        .renderer("heatmap")
                        .label("Chord Durations")
                        .asArray(timestamps)
                        .colorMapping(
                            d3.scaleLinear([0, 1], ["white", "darkorange"]),
                        ),
                )
                .column(
                    LineUpJS.buildCategoricalColumn("chords_reflecting_color")
                        .width(width_progression)
                        .label("Chords")
                        .categories([
                            { name: "C", color: cyclicHarmonicColoring(0) },
                            { name: "Db", color: cyclicHarmonicColoring(1) },
                            { name: "D", color: cyclicHarmonicColoring(2) },
                            { name: "Eb", color: cyclicHarmonicColoring(3) },
                            { name: "E", color: cyclicHarmonicColoring(4) },
                            { name: "F", color: cyclicHarmonicColoring(5) },
                            { name: "Gb", color: cyclicHarmonicColoring(6) },
                            { name: "G", color: cyclicHarmonicColoring(7) },
                            { name: "Ab", color: cyclicHarmonicColoring(8) },
                            { name: "A", color: cyclicHarmonicColoring(9) },
                            { name: "Bb", color: cyclicHarmonicColoring(10) },
                            { name: "B", color: cyclicHarmonicColoring(11) },
                        ])
                        .renderer(
                            "catheatmap",
                            "catheatmap",
                            "catdistributionbar",
                        )
                        .asArray(timestamps),
                )
                .column(
                    LineUpJS.buildNumberColumn("CC", [1, null])
                        .width(width_single_value)
                        .label("CC (Chord Coverage)")
                        .renderer("number")
                        .numberFormat(d3.format("d"))
                        .colorMapping(
                            d3.scaleLinear([0, 1], ["lightgrey", "darkgreen"]),
                        )
                        .htmlSummary(
                            "Number of differing chords used<br> <br> ",
                        ),
                )
                .column(
                    LineUpJS.buildNumberColumn("CHE", [0, null])
                        .width(width_single_value)
                        .label("CHE (Chord Histogram Entropy)")
                        .renderer("dot")
                        .colorMapping(
                            d3.scaleLinear([0, 1], ["lightgrey", "darkgreen"]),
                        )
                        .htmlSummary(
                            "0 - if only 1 chord is used<br>Increases when different chords are used",
                        ),
                ) // TODO get domain range, starts at 0 (for all is the same chord)
                .column(
                    LineUpJS.buildNumberColumn("PCS", [-1, 1])
                        .width(width_single_value)
                        .label("PCS average (pitch consonance score)")
                        .renderer("dot")
                        .colorMapping(
                            d3.scaleLinear(
                                [0, 0.5, 1],
                                ["darkred", "lightgrey", "darkblue"],
                            ),
                        )
                        .htmlSummary(
                            "negative PCS = overall dissonant relation of melody note and chord<br>positive PCS = overall consonant<br>PCS 0 = same amounts of dissonant and consonant intervals",
                        ),
                ) // normalized range, does not depend on number of chord tones
                .column(
                    LineUpJS.buildNumberColumn(
                        "PCS progression (pitch consonance score)",
                        [-1, 1],
                    )
                        .width(width_progression)
                        .asArray(timestamps)
                        .colorMapping(
                            d3.scaleLinear(
                                [0, 0.5, 1],
                                ["darkred", "white", "darkblue"],
                            ),
                        )
                        .htmlSummary(
                            "negative PCS = overall dissonant relation of melody note and chord<br>positive PCS = overall consonant<br>PCS 0 = same amounts of dissonant and consonant intervals",
                        ),
                ) // normalized range, does not depend on number of chord tones
                .column(
                    LineUpJS.buildNumberColumn(
                        "MCTD progression (melody tone chord tonal distance)",
                        [0, 3],
                    )
                        .width(width_progression)
                        .asArray(timestamps)
                        .colorMapping(
                            d3.scaleLinear([0, 1], ["white", "darkviolet"]),
                        ),
                )
                .column(
                    LineUpJS.buildNumberColumn("MCTD_average", [0, 3])
                        .width(width_single_value)
                        .label("MCTD average (melody chord tonal distance)")
                        .renderer("dot")
                        .colorMapping(
                            d3.scaleLinear([0, 1], ["lightgrey", "darkviolet"]),
                        ),
                )
                .column(
                    LineUpJS.buildNumberColumn("CTD_average", [0, 2])
                        .width(width_single_value)
                        .label("CTD average (chord tonal distance)")
                        .renderer("dot")
                        .colorMapping(
                            d3
                                .scaleLinear([0, 1], ["lightgrey", "darkblue"])
                                .unknown("lightgrey"),
                        ),
                ) // 0 for same chords, the bigger the value the bigger the change
                .column(
                    LineUpJS.buildNumberColumn(
                        "CTD per chord (chord tonal distance)",
                        [0, 2],
                    )
                        .width(width_progression)
                        .asArray(timestamps)
                        .colorMapping(
                            d3
                                .scaleLinear([0, 1], ["#ccc", "darkblue"])
                                .unknown("lightgrey"),
                        )
                        .htmlSummary(
                            "Tonal distance of a chord to its previous chord<br>First chord has no previous chord, therefore no CTD value as well<br>Chord beginnings are highlighted by a CTD value of 2",
                        ),
                )
                .column(
                    LineUpJS.buildNumberColumn(
                        "CT class progression (chord tone)",
                        [0, 1],
                    )
                        .width(width_progression)
                        .asArray(timestamps)
                        .renderer("heatmap", "default", "histogram")
                        .colorMapping(
                            d3.scaleLinear(
                                [0, 0.5, 1],
                                ["darkred", "white", "darkblue"],
                            ),
                        )
                        .htmlSummary(
                            "from left = dissonant tone (red), <br>proposition, scale, chord (blue)",
                        ),
                )
                //.column(LineUpJS.buildCategoricalColumn("CT class progression (chord tone) (string labels)").categories(["chord_tone", "non_chord_tone", "proper_non_chord_tone"]).asArray(timestamps))
                //.column(LineUpJS.buildCategoricalColumn('CT class progression (chord tone) (string labels)').asArray(timestamps).color('schemeCategory10').width(200)) // TODO probably not display it
                .column(
                    LineUpJS.buildNumberColumn("CTnCTR", [0, 1])
                        .width(width_single_value)
                        .renderer("dot")
                        .label("CTnCTR (chord tone to non chord tone ratio)")
                        .colorMapping(
                            d3.scaleLinear(
                                [0, 0.5, 1],
                                ["darkred", "lightgrey", "darkblue"],
                            ),
                        )
                        .htmlSummary(
                            "0 = red = only non chord tones<br> 1 = blue = only chord tones (or at least proper non chord tones)<br> ",
                        ),
                ) // range [0,1], 0 is only non-chord-tones, 1 is only chord-tones, or proper-non-chord-tones (proper in the sense of accepted non-chord-tones, because they are positively interesting)

                .column(
                    LineUpJS.buildCategoricalColumn("key")
                        .width(width_single_value)
                        .categories(KEYS.map((k) => k.name))
                        .label("Key"),
                )
                .column(
                    LineUpJS.buildActionsColumn()
                        .width(width_single_value / 3)
                        .actions([
                            {
                                name: "play",
                                icon: "▶",
                                action: (row) => {
                                    playHarmonization(row);
                                },
                            },
                        ])
                        .label("Play"),
                );
            /*
                .column(
                    LineUpJS.buildCategoricalColumn("AI_Model")
                        .label("AI model")
                        .width(width_single_value),
                )
                .column(
                    LineUpJS.buildNumberColumn("rythm_density", [0, 1])
                        .width(width_single_value)
                        .label("Rhythm Density")
                        .colorMapping(
                            d3.scaleLinear([0, 1], ["lightgrey", "darkblue"]),
                        ),
                );
                */

            // add all attributes within the provided data automatically and assign colors as well
            // do this to allow the user access to all data, even if it is not prepared to be displayed
            // also this enables having access to additional metrics (that might get added later) in lineup automatically (although the representation might not be good without manual adjustments)
            builder.deriveColumns().deriveColors();

            // renderer names to use for setting visualization types for the columns:
            // actions: new ActionRenderer(),
            // aggregate: new AggregateGroupRenderer(),
            // annotate: new AnnotationRenderer(),
            // boolean: new BooleanCellRenderer(),
            // boxplot: new BoxplotCellRenderer(),
            // brightness: new BrightnessCellRenderer(),
            // catdistributionbar: new CategoricalStackedDistributionlCellRenderer(),
            // categorical: new CategoricalCellRenderer(),
            // circle: new CircleCellRenderer(),
            // date: new DateCellRenderer(),
            // default: defaultCellRenderer,
            // dot: new DotCellRenderer(),
            // group: new GroupCellRenderer(),
            // heatmap: new HeatmapCellRenderer(),
            // catheatmap: new CategoricalHeatmapCellRenderer(),
            // histogram: new HistogramCellRenderer(),
            // datehistogram: new DateHistogramCellRenderer(),
            // image: new ImageCellRenderer(),
            // interleaving: new InterleavingCellRenderer(),
            // link: new LinkCellRenderer(),
            // linkMap: new LinkMapCellRenderer(),
            // loading: new LoadingCellRenderer(),
            // nested: new MultiLevelCellRenderer(false),
            // number: new BarCellRenderer(),
            // mapbars: new MapBarCellRenderer(),
            // rank: new RankCellRenderer(),
            // selection: new SelectionRenderer(),
            // set: new SetCellRenderer(),
            // sparkline: new SparklineCellRenderer(),
            // stack: new MultiLevelCellRenderer(),
            // string: new StringCellRenderer(),
            // stringhist: new StringHistogramCellRenderer(),
            // table: new TableCellRenderer(),
            // upset: new UpSetCellRenderer(),
            // verticalbar: new VerticalBarCellRenderer(),
            // violin: new ViolinPlotCellRenderer(),
            // tick: new TickCellRenderer(),
            // cattick: new CategoricalTickCellRenderer(),

            // add tailored rankings that are a good start into analysis
            // TODO first ranking without the progression versions due to first overview, and progressions have a lot more details already?
            const ranking_metrics_of_yeh = LineUpJS.buildRanking()
                .rank()
                .selection()
                .column("PCS average (pitch consonance score)")
                .column("PCS progression (pitch consonance score)")
                .column("CTnCTR (chord tone to non chord tone ratio)")
                .column("CT class progression (chord tone)")
                .column("MCTD average (melody chord tonal distance)")
                .column("MCTD progression (melody tone chord tonal distance)")
                .column("CTD average (chord tonal distance)")
                .column("CTD per chord (chord tonal distance)")
                .column("CC (Chord Coverage)")
                .column("CHE (Chord Histogram Entropy)")
                .column("Chords");

            const small_ranking = LineUpJS.buildRanking()
                .rank()
                .selection()
                .column("PCS progression (pitch consonance score)")
                .column("CT class progression (chord tone)")
                .column("MCTD progression (melody tone chord tonal distance)")
                .column("CTD per chord (chord tonal distance)")
                .column("Typical chord transition indication per chord")
                .column("Bass Tones (midi)");

            const functional_analysis = LineUpJS.buildRanking()
                .rank()
                .selection()
                .column("Rhythm Density")
                .column("Chords")
                .column("key")
                .column("Roman Numerals")
                .column("Typicality Percentage")
                .column("Typical chord transition indication per chord")
                .column("Bass Tones (midi)");

            const default_ranking = LineUpJS.buildRanking()
                .column("Play")
                .column("key")
                .column("Typicality Percentage")
                .column("Typical chord transition indication per chord")
                .column("CC (Chord Coverage)")
                .column("Chords")
                .column("Roman Numerals")
                .column("PCS average (pitch consonance score)")
                .column("PCS progression (pitch consonance score)")
                .column("CTnCTR (chord tone to non chord tone ratio)")
                .column("CT class progression (chord tone)")
                .column("MCTD average (melody chord tonal distance)")
                .column("MCTD progression (melody tone chord tonal distance)")
                .column("CTD average (chord tonal distance)")
                .column("CTD per chord (chord tonal distance)")
                .column("CHE (Chord Histogram Entropy)");

            builder
                //.ranking(functional_analysis)
                //.ranking(ranking_metrics_of_yeh)
                //.ranking(small_ranking)
                .ranking(default_ranking);
            //.defaultRanking();

            //builder.overviewMode(); // use that mode initially, to follow paradigm: overview first, zoom and filter, details on demand
            lineUp = builder.buildTaggle(container); // when using Taggle, there is an overview option that comes in handy for more samples than can fit in the screen
            lineUp.on("selectionChanged", selectionChangedListener);
            lineUp.on("highlightChanged", (dataIndex) => {
                music.highlighted_harmonization_index = dataIndex;
                if (dataIndex !== -1) {
                    // if a row is highlighted
                    music.highlighted_harmonization =
                        music.harmonizations[dataIndex];
                } else {
                    // nothing is highlighted
                    music.highlighted_harmonization = {};
                }
            });
        }
    });

    function addSelectionToLineUp(spacingDiv, row) {
        if (spacingDiv && !spacingDiv.querySelector("select")) {
            spacingDiv.textContent = "";
            const select = document.createElement("select");
            select.id = "key-select";

            // Populate options
            KEYS.map((v) => v.name).forEach((k) => {
                const opt = document.createElement("option");
                opt.value = k;
                opt.textContent = k;
                select.appendChild(opt);
            });

            // Set initial value
            select.value = music.harmonizations[row]?.key || "";

            // Listen to changes
            select.addEventListener("change", (e) => {
                updateKey(e, row);
            });

            spacingDiv.appendChild(select);

            const colorDiv = container.querySelector(
                'article[data-ranking="rank0"] div[data-i="' +
                    row +
                    '"] div[data-id="col1"] .lu-cat-color', //'section[title="Key"] .lu-spacing',
            );

            colorDiv.style.backgroundColor =
                KEYS.find((k) => k.name === select.value)?.color ||
                "transparent";

            recolorKeyDistribution();
        }
    }

    function recolorKeyDistribution() {
        const elements = container.querySelectorAll(
            'section[title="Key"] div[data-renderer="categorical"] div.lu-histogram-bin',
        );

        elements.forEach((el) => {
            const cat = el.getAttribute("data-cat");

            const entry = KEYS.find((k) => k.name === cat);
            if (!entry) return;

            el.querySelector("div").style.background = entry.color;
        });
    }

    function selectionChangedListener(selection) {
        selection.sort((a, b) => {
            return a - b;
        });
        selectedIndex.set(selection[0] ?? -1);
        music.selected_harmonizations_indeces = selection;
        music.selected_harmonizations = []; // get rid of not anymore selected
        for (let index of selection) {
            music.selected_harmonizations.push(music.harmonizations[index]);
        }
    }
</script>

<div id="lineup" class="lineup" bind:this={container}></div>

<style>
    /* width and height setting needed to get lineup to show up properly */
    .lineup {
        width: 100%;
        height: 100%;
        position: relative;
    }

    /* override overflow for all data cells */
    :global(.le-td) {
        overflow: hidden !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
        font-size: 14px !important;
        line-height: 18px !important;
    }

    :global(.lu-actions) {
        opacity: 1;
        visibility: visible;
        cursor: pointer;
    }

    :global(.le-tr.playing span[title="play"]) {
        color: #cca22e;
        font-weight: bold;
        transform: scale(1.2);
    }
</style>
