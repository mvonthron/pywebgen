# Copyright 2008 David Anderson
#
# Redistribution of this file is permitted under
# the terms of the GNU Public License (GPL) version 2.

"""Utility functions."""

__author__ = 'David Anderson <dave@natulte.net>'

import os.path

import error


class FileNotFoundError(error.Error):
    """The requested file does not exit."""

class FileEncodingError(error.Error):
    """The file's encoding is incorrectly specified."""

class PathObstructedError(error.Error):
    """The path references an existing non-file."""


def ReadFileContent(filename, codec='utf-8'):
    """Read and return the entire content of a file.

    By default, will automatically read the file as binary and
    interpret it as UTF-8 to create a Unicode string.

    Args:
      filename: the path to the file to read.
      codec: the encoding used in the file (default: utf-8).

    Returns:
      The full file contents as a unicode string.

    Raises:
      FileNotFoundError: the requested file does not exist.
      FileEncodingError: the given codec could not decode the file
                         content.
      IOError: an error occured while reading the file.
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    f = open(filename, 'rb')
    content = f.read()
    f.close()

    try:
        return content.decode(codec)
    except UnicodeDecodeError:
        raise FileEncodingError(filename)


def WriteFileContent(filename, content, codec='utf-8'):
    """Write the given content to a file.

    The content is assumed to a unicode object, and will be encoded
    using the given codec (defaults to UTF-8). If the file already
    exists, it is overwritten.

    Args:
      filename: the path to the file to write.
      content: the unicode content to write.
      codec: the encoding to use in the file (default: utf-8).

    Raises:
      PathObstructedError: a non-file exists at the given path.
      FileEncodingError: translation using the given codec failed.
      IOError: an error occured while writing the file.
    """
    if os.path.exists(filename) and not os.path.isfile(filename):
        raise PathObstructedError(filename)

    try:
        content = content.encode(codec)
    except UnicodeEncodeError:
        raise FileEncodingError(filename)

    f = open(filename, 'wb')
    f.write(content)
    f.close()


def PathAsSuffix(path, root):
    """Return path, with the root stripped off.

    Args:
      path: the full path.
      root: the path prefix to strip.

    Returns:
      The path suffix.

    Raises:
      AssertionError: root is not a prefix of path.
    """
    assert path.startswith(root)
    suffix = path[len(root):]
    if suffix.startswith('/'):
        suffix = suffix[1:]
    return suffix


def RelocatePath(path, orig_root, new_root):
    """Compute a path's new location under a new root directory.

    Args:
      path: the path to relocate.
      orig_root: the prefix of path that is the original root.
      new_root: the new relocated prefix.

    Returns:
      The relocated path.

    Raises:
      AssertionError: orig_root is not a prefix of path.
    """
    suffix = PathAsSuffix(path, orig_root)
    return os.path.join(new_root, suffix)


def CreateDir(path):
    """Create a directory, if it does not already exist.

    This function recursively creates directories as needed.

    Args:
      path: the directory to create.

    Raises:
      PathObstructedError: the given path is obstructed by a non-dir.
    """
    if os.path.exists(path) and not os.path.isdir(path):
        raise PathObstructedError(path)

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except os.error:
            raise PathObstructedError(path)
