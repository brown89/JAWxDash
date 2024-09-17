inch2mm = 25.4



wafer_4in = dict(
    type='circle',
    x0=-2*inch2mm,
    y0=-2*inch2mm,
    x1=2*inch2mm,
    y1=2*inch2mm,
    line=dict(
        color="rgba(1, 0, 0, 1)",
        width=1,
        dash='solid',
    ),
    fillcolor="rgba(0, 0, 0, 0)",
    name="sample_outline",
)

wafer_6in = dict(
    type='circle',
    x0=-3*inch2mm,
    y0=-3*inch2mm,
    x1=3*inch2mm,
    y1=3*inch2mm,
    line=dict(
        color="rgba(1, 0, 0, 1)",
        width=1,
        dash='solid',
    ),
    fillcolor="rgba(0, 0, 0, 0)",
    name="sample_outline",
)

wafer_8in = dict(
    type='circle',
    x0=-4*inch2mm,
    y0=-4*inch2mm,
    x1=4*inch2mm,
    y1=4*inch2mm,
    line=dict(
        color="rgba(1, 0, 0, 1)",
        width=1,
        dash='solid',
    ),
    fillcolor="rgba(0, 0, 0, 0)",
    name="sample_outline",
)



sample_outlines = {
    "wafer 4 inch": wafer_4in,
    "wafer 6 inch": wafer_6in,
    "wafer 8 inch": wafer_8in,
}
