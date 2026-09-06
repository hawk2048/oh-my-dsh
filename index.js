// oh-my-dsh bundle entry.
//
// The bundle is a composition layer (`cordis.patch.yml`), not a top-level
// plugin; its capability modules live under ./commands and its skills under
// ./skills. This entry exists so the package resolves as a module for the
// patch rows that reference `oh-my-dsh/commands`; it intentionally exports
// nothing.
export {}
