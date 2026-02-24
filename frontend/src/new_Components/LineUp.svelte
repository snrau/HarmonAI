<link href="https://unpkg.com/lineupjs/build/LineUpJS.css" rel="stylesheet">
<!-- <link href="http://127.0.0.1:5000/lineupcss-sourcemap-file" rel="stylesheet"> -->
<script src="https://unpkg.com/lineupjs/build/LineUpJS.js">
    import {music, process_harmonizations_for_visualization, smallest_duration_considered} from "../state.svelte.js";

    import * as LineUpJS from "lineupjs";
    import * as d3 from "d3";

    let container;
    //let container2;

    let lineUp;

    //const smallest_duration_considered = 0.25; // should be 1/16 note duration, based on a quarter note length that is 1.
    //
    // function process_harmonizations_for_lineUp(harmonizations) {
    //     let processed_harmonizations = [];
    //
    //     for (let harmonization of harmonizations) {
    //         let processed_harmonization = {};
    //         // in the following add attributes that need processing for useful visual representation in lineup
    //
    //         let MCTD_progression = [];
    //         let CT_class_progression = [];
    //         let CT_class_progression_string = [];
    //         let PCS_progression = [];
    //         let CT_class_as_numerical_value = {
    //             "chord_tone": 0,
    //             "non_chord_tone": 0.7,
    //             "proper_non_chord_tone": 1,
    //         }
    //         // encode durations as well
    //         // consider each pair of melody tone and corresponding chord, this is not just the number of chords or melody notes
    //         for (let i = 0; i < harmonization["MCTD_progression"].length; i++) {
    //             let number_of_needed_duplicates = (harmonization["MCTD_progression"][i]["end"] - harmonization["MCTD_progression"][i]["start"]) / smallest_duration_considered;
    //             for (let j = 0; j < number_of_needed_duplicates; j++) {
    //                 MCTD_progression.push(harmonization["MCTD_progression"][i]["MCTD"]);
    //                 CT_class_progression.push(CT_class_as_numerical_value[harmonization["CT_class_progression"][i]["class"]]);
    //                 CT_class_progression_string.push(harmonization["CT_class_progression"][i]["class"]);
    //                 PCS_progression.push(harmonization["PCS_progression"][i]["score"]);
    //             }
    //         }
    //         processed_harmonization["MCTD progression (melody tone chord tonal distance)"] = MCTD_progression;
    //         processed_harmonization["CT class progression (chord tone)"] = CT_class_progression;
    //         processed_harmonization["CT class progression (chord tone) (string labels)"] = CT_class_progression_string;
    //         processed_harmonization["PCS progression (pitch consonance score)"] = PCS_progression;
    //
    //         //reflect chord durations as well
    //         // oriented on the number of chords in the respective harmonization
    //         let chords = [];
    //         let chord_durations = [];
    //         let bass_notes_midi = [];
    //         let typicality_of_chords = [];
    //         let CTDs = [];
    //         for (let i = 0; i < harmonization["chord_symbols"].length; i++) {
    //             let number_of_needed_duplicates = harmonization["chord_durations"][i] / smallest_duration_considered;
    //             for (let j = 0; j < number_of_needed_duplicates; j++) {
    //                 chords.push(harmonization["chord_symbols"][i]);
    //                 chord_durations.push(harmonization["chord_durations"][i]);
    //                 bass_notes_midi.push(harmonization["chords_bass_note_midi"][i]);
    //                 typicality_of_chords.push(harmonization["typical_chord_progression_coverage_per_chord"][i]);
    //                 if (j === number_of_needed_duplicates - 1 && harmonization["CTD_per_chord"][i]) {
    //                     CTDs.push(2); // to highlight chord beginnings visually
    //                 } else {
    //                     CTDs.push(harmonization["CTD_per_chord"][i]);
    //                 }
    //             }
    //         }
    //         processed_harmonization["chords_reflecting_durations"] = chords;
    //         processed_harmonization["chord_durations_reflecting_durations"] = chord_durations;
    //         processed_harmonization["chords_bass_note_midi_reflecting_durations"] = bass_notes_midi;
    //         processed_harmonization["typicality_of_chords_per_chord"] = typicality_of_chords;
    //         processed_harmonization["CTD per chord (chord tonal distance)"] = CTDs;
    //
    //         // keep all data available but implement default selection of columns that seem most useful and others the user can add manually if wanted?
    //         // ai model specific attributes (as e.g. rhythm density) of harmonizers added in the future could not be considered here, only if all attributes are kept and manual pre-selection of columns is done
    //         for (let key in harmonization) {
    //             processed_harmonization[key] = harmonization[key]; // add all attributes unchanged
    //         }
    //
    //         processed_harmonizations.push(processed_harmonization);
    //     }
    //
    //     //music.harmonizations = processed_harmonizations; // DONT DO THAT, it leads to a probably infinite loop of updating harmonizations
    //     return processed_harmonizations;
    // }

    $effect(() => {
        if (music.harmonizations.length === 0) {
            // inform user that first harmonizations are needed
            document.getElementById("lineup").innerHTML = "No data available to show in lineup.";
        } else {
            //change of innerHTML needs to come before adding lineup for some reason
            document.getElementById("lineup").innerHTML = "";
            //document.getElementById("lineup2").innerHTML = "";

            // give the user a default view that is tailored to the data
            // lineup allows the user anyway to modify the representation
            //const lineup2 = LineUpJS.asTaggle(container2, process_harmonizations_for_lineUp(music.harmonizations));
            const builder = LineUpJS.builder(process_harmonizations_for_visualization(music.harmonizations));

            // prepare for and manually define columns
            let piece_duration = music.harmonizations[0]["chord_starting_times"][music.harmonizations[0]["chord_starting_times"].length - 1] + music.harmonizations[0]["chord_durations"][music.harmonizations[0]["chord_durations"].length - 1];
            let total_number_of_timestamps = piece_duration / smallest_duration_considered;
            let timestamps = Array(total_number_of_timestamps);
            for (let i = 0; i < timestamps.length; i++) {
                timestamps[i] = i * smallest_duration_considered + " Quarter notes from beginning";
            }

            const binary_color = (v) => v === 1 ? "darkcyan" : '#aaa';

            const width_single_value = 60;
            const width_progression = 250;

            builder
                .column(LineUpJS.buildNumberColumn('typicality_of_chords_per_chord', [0, 1])
                    .width(width_progression)
                    .label("Typical chord transition indication per chord")
                    .colorMapping(binary_color)
                    .asArray(timestamps)
                    .renderer("heatmap")
                    .htmlSummary("either 0 or 1<br>0 = not part of a typical chord progression<br>1 = part of a typical chord progression")
                )
                .column(LineUpJS.buildCategoricalColumn('roman_numerals')
                    .width(width_single_value)
                    .label("Roman Numerals (String)")
                    .renderer("string", "default", "categorical")
                    .asArray(timestamps)
                )
                .column(LineUpJS.buildCategoricalColumn('roman_numerals_reflecting_durations')
                    .width(width_progression)
                    .label("Roman Numerals")
                    .renderer("catheatmap", "catheatmap", "catdistributionbar")
                    .asArray(timestamps)
                )
                .column(LineUpJS.buildNumberColumn('typical_chord_progression_coverage', [0, 100])
                    .width(width_single_value)
                    .label("Typicality Percentage")
                    .colorMapping(d3.scaleLinear([0, 1], ["#aaa", "darkcyan"]))
                    .htmlSummary("in %<br>0% = no typical transition<br>100% = entirely consisting of typical transitions")
                )
                .column(LineUpJS.buildNumberColumn('chords_bass_note_midi_reflecting_durations')
                    .width(width_progression)
                    .renderer("sparkline")
                    .label("Bass Tones (midi)")
                    .asArray(timestamps)
                )
                .column(LineUpJS.buildNumberColumn('chord_durations_reflecting_durations')
                    .width(width_progression)
                    .renderer("heatmap")
                    .label("Chord Durations")
                    .asArray(timestamps)
                    .colorMapping(d3.scaleLinear([0, 1], ["white", "darkorange"]))
                )
                .column(LineUpJS.buildCategoricalColumn('chords_reflecting_durations')
                    .width(width_progression)
                    .label("Chords")
                    .renderer("catheatmap", "catheatmap", "catdistributionbar")
                    .asArray(timestamps)
                )
                .column(LineUpJS.buildNumberColumn('CC', [1, null])
                    .width(width_single_value)
                    .label("CC (Chord Coverage)")
                    .colorMapping(d3.scaleLinear([0, 1], ["lightgrey", "darkgreen"]))
                    .htmlSummary("Number of differing chords used<br> <br> ")
                )
                .column(LineUpJS.buildNumberColumn('CHE', [0, null])
                    .width(width_single_value)
                    .label("CHE (Chord Histogram Entropy)")
                    .colorMapping(d3.scaleLinear([0, 1], ["lightgrey", "darkgreen"]))
                    .htmlSummary("0 - if only 1 chord is used<br>Increases when different chords are used")
                ) // TODO get domain range, starts at 0 (for all is the same chord)
                .column(LineUpJS.buildNumberColumn('PCS', [-1, 1])
                    .width(width_single_value)
                    .label("PCS average (pitch consonance score)")
                    .renderer("tick")
                    .colorMapping(d3.scaleLinear([0, 0.5, 1], ["darkred", "lightgrey", "darkblue"]))
                    .htmlSummary("negative PCS = overall dissonant relation of melody note and chord<br>positive PCS = overall consonant<br>PCS 0 = same amounts of dissonant and consonant intervals")
                ) // normalized range, does not depend on number of chord tones
                .column(LineUpJS.buildNumberColumn('PCS progression (pitch consonance score)', [-1, 1])
                    .width(width_progression)
                    .asArray(timestamps)
                    .colorMapping(d3.scaleLinear([0, 0.5, 1], ["darkred", "white", "darkblue"]))
                    .htmlSummary("negative PCS = overall dissonant relation of melody note and chord<br>positive PCS = overall consonant<br>PCS 0 = same amounts of dissonant and consonant intervals")
                ) // normalized range, does not depend on number of chord tones
                .column(LineUpJS.buildNumberColumn('MCTD progression (melody tone chord tonal distance)', [0, 3])
                    .width(width_progression)
                    .asArray(timestamps)
                    .colorMapping(d3.scaleLinear([0, 1], ["white", "darkviolet"]))
                )
                .column(LineUpJS.buildNumberColumn('MCTD_average', [0, 3])
                    .width(width_single_value)
                    .label("MCTD average (melody chord tonal distance)")
                    .colorMapping(d3.scaleLinear([0, 1], ["lightgrey", "darkviolet"]))
                )
                .column(LineUpJS.buildNumberColumn('CTD_average', [0, 2])
                    .width(width_single_value)
                    .label("CTD average (chord tonal distance)")
                    .colorMapping(d3.scaleLinear([0, 1], ["lightgrey", "darkblue"]).unknown("lightgrey"))
                ) // 0 for same chords, the bigger the value the bigger the change
                .column(LineUpJS.buildNumberColumn('CTD per chord (chord tonal distance)', [0, 2])
                    .width(width_progression)
                    .asArray(timestamps)
                    .colorMapping(d3.scaleLinear([0, 1], ["#ccc", "darkblue"]).unknown("lightgrey"))
                    .htmlSummary("Tonal distance of a chord to its previous chord<br>First chord has no previous chord, therefore no CTD value as well<br>Chord beginnings are highlighted by a CTD value of 2")
                )

                .column(LineUpJS.buildNumberColumn('CT class progression (chord tone)', [0, 1])
                    .width(width_progression)
                    .asArray(timestamps)
                    .renderer("heatmap", "default", "histogram")
                    .colorMapping(d3.scaleLinear([0, 0.5, 1], ["darkblue", "darkorange", "darkred"]))
                    .htmlSummary("blue = chord tone<br> orange = proper non chord tone (kind of accepted non chord tone)<br> red = non chord tone")
                    .description("0 = chord tone; 0.5 = proper non chord tone (kind of accepted non chord tone); 1 = non chord tone")
                )
                //.column(LineUpJS.buildCategoricalColumn("CT class progression (chord tone) (string labels)").categories(["chord_tone", "non_chord_tone", "proper_non_chord_tone"]).asArray(timestamps))
                //.column(LineUpJS.buildCategoricalColumn('CT class progression (chord tone) (string labels)').asArray(timestamps).color('schemeCategory10').width(200)) // TODO probably not display it
                .column(LineUpJS.buildNumberColumn('CTnCTR', [0, 1])
                    .width(width_single_value)
                    .renderer("tick")
                    .label("CTnCTR (chord tone to non chord tone ratio)")
                    .colorMapping(d3.scaleLinear([0, 0.5, 1], ["darkred", "lightgrey", "darkblue"]))
                    .htmlSummary("0 = red = only non chord tones<br> 1 = blue = only chord tones (or at least proper non chord tones)<br> ")
                ) // range [0,1], 0 is only non-chord-tones, 1 is only chord-tones, or proper-non-chord-tones (proper in the sense of accepted non-chord-tones, because they are positively interesting)

                .column(LineUpJS.buildCategoricalColumn('AI_Model')
                    .label('AI model')
                    .width(width_single_value)
                )
                .column(LineUpJS.buildNumberColumn('rythm_density', [0, 1])
                    .width(width_single_value)
                    .label("Rhythm Density")
                    .colorMapping(d3.scaleLinear([0, 1], ["lightgrey", "darkblue"]))
                );

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
                .column("Chords")

            const small_ranking = LineUpJS.buildRanking()
                .rank()
                .selection()
                .column("PCS progression (pitch consonance score)")
                .column("CT class progression (chord tone)")
                .column("MCTD progression (melody tone chord tonal distance)")
                .column("CTD per chord (chord tonal distance)")
                .column("Typical chord transition indication per chord")
                .column("Bass Tones (midi)")

            const functional_analysis = LineUpJS.buildRanking()
                .rank()
                .selection()
                .column("Rhythm Density")
                .column("Chords")
                .column("key")
                .column("Roman Numerals")
                .column("Typicality Percentage")
                .column("Typical chord transition indication per chord")
                .column("Bass Tones (midi)")


            builder
                .ranking(functional_analysis)
                .ranking(ranking_metrics_of_yeh)
                .ranking(small_ranking)
                .defaultRanking();

            builder.overviewMode(); // use that mode initially, to follow paradigm: overview first, zoom and filter, details on demand
            lineUp = builder.buildTaggle(container); // when using Taggle, there is an overview option that comes in handy for more samples than can fit in the screen
            lineUp.on("selectionChanged", selectionChangedListener)
            lineUp.on("highlightChanged", (dataIndex) => {
                music.highlighted_harmonization_index = dataIndex;
                if (dataIndex !== -1) {
                    // if a row is highlighted
                    music.highlighted_harmonization = music.harmonizations[dataIndex];
                } else {
                    // nothing is highlighted
                    music.highlighted_harmonization = {};
                }
            })
        }
    });

    function selectionChangedListener(selection) {
        selection.sort((a, b) => {
            return a - b
        });
        music.selected_harmonizations_indeces = selection;
        music.selected_harmonizations = []; // get rid of not anymore selected
        for (let index of selection) {
            music.selected_harmonizations.push(music.harmonizations[index]);
        }
    }
</script>


<div id="lineup" class="lineup" bind:this={container}>No data available to show in lineup.</div>
<!--
<h2>LineUp 2</h2>
<div id="lineup2" class="lineup" bind:this={container2}>No data available to show in lineup.</div>
-->

<style>
    /* width and height setting needed to get lineup to show up properly */
    .lineup {
        width: 100%;
        height: 100%;
    }
</style>

