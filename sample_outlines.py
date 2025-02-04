INCH2MM = 25.4
INCH2CM = 2.54


def wafer_inch(dia_inch:float) -> dict:
    r_inch = 0.5 * dia_inch
    return dict(
        type='circle',
        x0=-r_inch*INCH2CM,
        y0=-r_inch*INCH2CM,
        x1=r_inch*INCH2CM,
        y1=r_inch*INCH2CM,
        line=dict(
            color="rgba(1, 0, 0, 1)",
            width=1,
            dash='solid',
        ),
        fillcolor="rgba(0, 0, 0, 0)",
        name="sample_outline",
    )


sample_outlines = {
    "wafer 4 inch": wafer_inch(4),
    "wafer 6 inch": wafer_inch(6),
    "wafer 8 inch": wafer_inch(8),
}
