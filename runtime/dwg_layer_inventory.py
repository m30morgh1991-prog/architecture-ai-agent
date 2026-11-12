from __future__ import annotations

from collections.abc import Iterable


def resolve_source_layer_names(
    modelspace_handles: set[int],
    entity_style_rows: Iterable[tuple[int, int | None, int | None, int | None]],
    layer_rows: Iterable[tuple[int, str]],
) -> tuple[list[str], list[int]]:
    """Resolve modelspace layer names through DWG layer handles.

    ezdwg's raw common-entity style rows expose layer handles; the layer table
    maps those handles to names. Missing links are returned explicitly rather
    than silently inventing layer "0".
    """
    layer_by_handle = {int(handle): str(name) for handle, name in layer_rows}
    layer_handle_by_entity = {
        int(handle): layer_handle
        for handle, _color, _true_color, layer_handle in entity_style_rows
    }
    names: set[str] = set()
    unresolved: list[int] = []
    for handle in sorted(modelspace_handles):
        layer_handle = layer_handle_by_entity.get(handle)
        if layer_handle is None:
            unresolved.append(handle)
            continue
        name = layer_by_handle.get(int(layer_handle))
        if name is None:
            unresolved.append(handle)
            continue
        names.add(name)
    return sorted(names), unresolved
