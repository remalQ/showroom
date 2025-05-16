#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file scrollable_tab.py
@brief Utility to create a vertically scrollable frame in Tkinter.

This module provides a function to embed a scrollable area within
a parent widget, with mouse-wheel support.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import Widget


def make_scrollable_tab(parent: Widget) -> ttk.Frame:
    """
    \brief Create and return a scrollable frame inside the given parent.

    \param[in] parent The container widget where the scrollable frame is placed.
    \return A ttk.Frame instance that supports vertical scrolling.
    """
    # Create canvas and scrollbar
    canvas = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(
        parent,
        orient='vertical',
        command=canvas.yview
    )

    # Frame that will be scrolled
    scrollable_container = ttk.Frame(canvas)

    def _on_configure(event: tk.Event) -> None:
        """
        \brief Update scroll region when the inner frame size changes.
        """
        canvas.configure(scrollregion=canvas.bbox('all'))

    scrollable_container.bind(
        '<Configure>',
        _on_configure
    )

    # Embed the scrollable container into the canvas
    canvas.create_window(
        (0, 0),
        window=scrollable_container,
        anchor='nw'
    )
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack canvas and scrollbar
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    def _on_mousewheel(event: tk.Event) -> None:
        """
        \brief Scroll canvas content on mouse wheel events.
        """
        canvas.yview_scroll(-int(event.delta / 120), 'units')

    canvas.bind_all(
        '<MouseWheel>',
        _on_mousewheel
    )

    return scrollable_container
